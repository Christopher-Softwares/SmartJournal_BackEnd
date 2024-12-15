from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from workspace.models import Workspace
from workspace.serializers import AddMembersSerializer, WorkspaceDetailSerializer, RemoveMemberSerializer
from django.shortcuts import get_object_or_404

class WorkspaceViewSet(viewsets.ModelViewSet):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceDetailSerializer

class GetOwnedWorkspaces(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WorkspaceDetailSerializer
    def get(self, request):
        user = request.user
        owned_workspaces = Workspace.objects.filter(owner=user)
        serializer = self.serializer_class(owned_workspaces, many=True)

        return Response({"data": serializer.data}, status=200)

class GetMemberWorkspaces(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WorkspaceDetailSerializer
    def get(self, request):
        user = request.user
        member_workspaces = Workspace.objects.filter(members__id=user.id)
        serializer = WorkspaceDetailSerializer(member_workspaces, many=True)

        return Response({"data": serializer.data}, status=200)

class AddMembersToWorkspaceView(APIView):
    serializer_class = AddMembersSerializer
    def post(self, request, workspace_id):
        workspace = get_object_or_404(Workspace, id=workspace_id)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        member_ids = serializer.validated_data['member_ids']
        members_to_add = workspace.members.model.objects.filter(id__in=member_ids) 
        workspace.members.add(*members_to_add)

        return Response(
            {"message": "Members added successfully."},
            status=status.HTTP_200_OK
        )

class RemoveMembersAPIView(APIView):
    serializer_class = RemoveMemberSerializer
    def post(self, request, workspace_id):
        workspace = get_object_or_404(Workspace, id=workspace_id)
        serializer = self.serializer_class(data=request.data, context={'workspace': workspace})
        serializer.is_valid(raise_exception=True)
        member_ids = serializer.validated_data['member_ids']
        members_to_remove = workspace.members.filter(id__in=member_ids)
        workspace.members.remove(*members_to_remove)

        return Response({"status": "Members removed successfully"}, status=status.HTTP_200_OK)
