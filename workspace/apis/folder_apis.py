from utils.response_wrapper import (
    StandardListAPIView, 
    StandardCreateAPIView,
    StandardDestroyAPIView,
    StandardUpdateAPIView,
    standard_response
) 
from django.shortcuts import get_object_or_404
from workspace.models import Workspace, Folder
from workspace.serializers import CreateFolderSerializer, UpdateFolderSerializer, FolderSerializer
from workspace import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework import status


class CreateFolderAPIView(StandardCreateAPIView):
    serializer_class = CreateFolderSerializer
    permission_classes = [IsAuthenticated, permissions.IsWorkspaceOwnerOrMember]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        workspace_id = serializer.validated_data.get("workspace_id")
        workspace = Workspace.objects.get(id=workspace_id)
        
        self.check_object_permissions(request, workspace)

        folder = serializer.save()
        
        return standard_response(
            data={
                "folder_id": folder.id
            },
            is_success=True,
            status_code=status.HTTP_201_CREATED
        )


class UpdateFolderAPIView(StandardUpdateAPIView):
    serializer_class = UpdateFolderSerializer
    permission_classes = [IsAuthenticated, permissions.IsWorkspaceOwnerOrMember]
    
    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        
        folder_id = serializer.validated_data["folder_id"]
        folder = get_object_or_404(Folder, id=folder_id)

        workspace = folder.workspace
        self.check_object_permissions(request, workspace)
        
        folder.title = serializer.validated_data["folder_name"]
        folder.save()
    
        return standard_response(
            data={
                "folder_id": folder.id
            },
            is_success=True,
            status_code=status.HTTP_200_OK
        )    


class DeleteFolderAPIView(StandardDestroyAPIView):
    """
    gets folder id and delete it if it's empty
    """
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer
    permission_classes = [IsAuthenticated, permissions.IsWorkspaceOwnerOrMember]
    
    def get_object(self):
        folder_id = self.kwargs["pk"]
        
        folder = get_object_or_404(Folder, id=folder_id)
        
        self.check_object_permissions(self.request, folder.workspace)
        
        return folder
    
    def perform_destroy(self, instance):
        if instance.notes.exists():
            raise ValidationError("Folder is not empty.")
        
        instance.delete()
