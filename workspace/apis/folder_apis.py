from utils.response_wrapper import (
    StandardListAPIView, 
    StandardCreateAPIView,
    StandardDestroyAPIView,
    StandardUpdateAPIView,
    standard_response
) 
from django.shortcuts import get_object_or_404
from workspace.models import Workspace, Tag, Page, Folder
from workspace.serializers import CreateFolderSerializer, UpdateFolderSerializer
from workspace import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework import status


class CreateFolderAPIView(StandardCreateAPIView):
    serializer_class = CreateFolderSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
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
    permission_classes = [IsAuthenticated]
    
    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        
        folder_id = serializer.validated_data["folder_id"]
        folder = get_object_or_404(Folder, id=folder_id)
        
        folder.name = serializer.validated_data["folder_name"]
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
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        folder_id = self.kwargs["pk"]
        
        folder = get_object_or_404(Folder, id=folder_id)
        
        return folder
    
    def perform_destroy(self, instance):
        if instance.pages.exists():
            raise ValidationError("Folder is not empty.")
        
        instance.delete()
