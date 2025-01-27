from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from workspace.models import Workspace
from workspace.serializers import AddMembersSerializer, WorkspaceSerializer, RemoveMemberSerializer
from django.shortcuts import get_object_or_404
from users.models import CustomUser

class WorkspaceViewSet(viewsets.ModelViewSet):
    print("man injam")
    # queryset = Workspace.objects.all()
    # serializer_class = WorkspaceSerializer
    # permission_classes = [IsAuthenticated]

class GetOwnedWorkspaces(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WorkspaceSerializer
    def get(self, request):
        user = request.user
        owned_workspaces = Workspace.objects.filter(owner=user)
        serializer = self.serializer_class(owned_workspaces, many=True)

        return Response({"data": serializer.data}, status=200)

class GetMemberWorkspaces(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WorkspaceSerializer
    def get(self, request):
        user = request.user
        member_workspaces = Workspace.objects.filter(members__id=user.id)
        serializer = self.serializer_class(member_workspaces, many=True)

        return Response({"data": serializer.data}, status=200)

class AddMembersToWorkspaceView(APIView):
    serializer_class = AddMembersSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, workspace_id):
        workspace = get_object_or_404(Workspace, id=workspace_id)

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        member_emails = serializer.validated_data['member_emails']

        plan = request.user.user_plan
        if not plan.can_add_member(workspace, len(member_emails)):
            return Response(
                {"message": "Exceeded the member count limit."},
                status=status.HTTP_402_PAYMENT_REQUIRED
            )
        members_to_add = CustomUser.objects.filter(email__in=member_emails)
        if len(members_to_add) != len(member_emails):
            return Response(
                {"message": "Some members not found."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Add the members to the workspace
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
        member_emails = serializer.validated_data['member_emails']
        members_to_remove = workspace.members.filter(email__in=member_emails)
        workspace.members.remove(*members_to_remove)

        return Response({"status": "Members removed successfully"}, status=status.HTTP_200_OK)
