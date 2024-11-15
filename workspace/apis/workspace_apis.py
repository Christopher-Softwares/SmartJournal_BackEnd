from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from workspace.models import Workspace
from rest_framework.permissions import IsAuthenticated
from workspace.permissions import IsOwnerOrReadOnly, IsMember
from workspace.serializers import (
    WorkspaceCreateSerializer,
    WorkspaceDetailSerializer,
    AddMemberSerializer,
    RemoveMemberSerializer,
    AddPageSerializer,
    RemovePageSerializer,
)

class WorkspaceViewSet(viewsets.ModelViewSet):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceDetailSerializer  # Default serializer
     
    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            permission_classes = [IsOwnerOrReadOnly]

        elif self.action in ['partial_update', 'update', 'add_members', 'remove_members', 'add_pages', 'remove_pages']:
            permission_classes = [IsMember, IsOwnerOrReadOnly]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'create':
            return WorkspaceCreateSerializer
        elif self.action == 'add_members':
            return AddMemberSerializer
        elif self.action == 'remove_members':
            return RemoveMemberSerializer
        elif self.action == 'add_pages':
            return AddPageSerializer
        elif self.action == 'remove_pages':
            return RemovePageSerializer
        return WorkspaceDetailSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=False, methods=['get'])
    def my_workspaces(self, request):
        user = request.user
        workspaces = Workspace.objects.filter(owner = user)
        serialized_data = self.serializer_class(workspaces, many = True)
        if serialized_data:
            return Response({'data': serialized_data.data}, status=status.HTTP_200_OK)
        return Response(status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def add_members(self, request, pk=None):
        workspace = self.get_object()
        serializer = self.get_serializer(workspace, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"status": "members added"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def remove_members(self, request, pk=None):
        workspace = self.get_object()
        serializer = self.get_serializer(workspace, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"status": "members removed"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def add_pages(self, request, pk=None):
        workspace = self.get_object()
        serializer = self.get_serializer(workspace, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"status": "pages added"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def remove_pages(self, request, pk=None):
        workspace = self.get_object()
        serializer = self.get_serializer(workspace, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"status": "pages removed"}, status=status.HTTP_200_OK)
