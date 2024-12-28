from utils.response_wrapper import (
    StandardListAPIView, 
    StandardCreateAPIView,
    StandardDestroyAPIView,
    StandardUpdateAPIView,
    standard_response
) 
from django.shortcuts import get_object_or_404
from workspace.models import Workspace
from note.serializers import TagSerializer, CreateTagSerializer, UpdateTagSerializer, TagAttachDetachSerializer
from note import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework import status
from note.models import Note, Tag


class GetWorkspaceTagsAPIView(StandardListAPIView):
    """
    Retrieve all tags of a specific workspace.
    Only accessible to the workspace owner or collaborators.
    """
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated, permissions.IsWorkspaceOwnerOrMember]

    def get_queryset(self):
        workspace_id = self.kwargs.get("workspace_id")
        workspace = get_object_or_404(Workspace, id=workspace_id)

        self.check_object_permissions(self.request, workspace)

        return workspace.tags.all()
    
    
class CreateTagAPIView(StandardCreateAPIView):
    """
    Create a tag for a specific workspace.
    Only workspace owners or collaborators can create tags.
    """
    serializer_class = CreateTagSerializer
    permission_classes = [IsAuthenticated, permissions.IsWorkspaceOwnerOrMember]

    def perform_create(self, serializer):
        return serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        workspace_id = serializer.validated_data.get("workspace_id")
        workspace = Workspace.objects.get(id=workspace_id)
        
        self.check_object_permissions(request, workspace)
        
        tag = self.perform_create(serializer)

        return standard_response(
            data={
                "tag_id": tag.id,
            },
            status_code=status.HTTP_201_CREATED
        )



class DeleteTagAPIView(StandardDestroyAPIView):
    """
    Delete a specific tag.
    Only the owner of the workspace can delete tags.
    """
    queryset = Tag.objects.all()
    permission_classes = [IsAuthenticated, permissions.HasTagInWorkspace]
    serializer_class = TagSerializer

    def get_object(self):
        tag = super().get_object()
        workspace = tag.workspace

        return tag 


class UpdateTagAPIView(StandardUpdateAPIView):
    """
    Update a specific tag.
    Only the owner of the workspace or collaborators can update tags.
    """
    queryset = Tag.objects.all()
    serializer_class = UpdateTagSerializer
    permission_classes = [IsAuthenticated, permissions.HasTagInWorkspace]

    def get_object(self):
        tag_id = self.request.data.get("id")
        try:
            return Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            return None

    def update(self, request, *args, **kwargs):
        tag = self.get_object()
        
        self.check_object_permissions(self.request, tag)
        
        if not tag:
            return standard_response(errors={"message": "Tag with the given ID does not exist."},
                            status_code=status.HTTP_404_NOT_FOUND, is_success=False)

        serializer = self.get_serializer(tag, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return standard_response(
            data={"id": serializer.instance.id},
            status_code=status.HTTP_200_OK,
        )
        

class AttachPageToTagAPIView(GenericAPIView):
    """
    Attach a page to a tag.
    Only authorized users (owner or collaborators) can attach a page to a tag.
    """
    permission_classes = [IsAuthenticated, permissions.HasNoteInWorkspace, permissions.HasTagInWorkspace]
    serializer_class = TagAttachDetachSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            tag_id = serializer.validated_data.get("tag_id")
            note_id = serializer.validated_data.get("note_id")
            
            note = Note.objects.get(id=note_id)
            tag = Tag.objects.get(id=tag_id)
            
            self.check_object_permissions(request, note)
            self.check_object_permissions(request, tag)
            
            serializer.attach_tag_to_note()
            return standard_response(data={"message": "Tag attached successfully."}, status_code=status.HTTP_200_OK)
        return standard_response(errors=serializer.errors, is_success=False, status_code=status.HTTP_400_BAD_REQUEST)


class DetachPageFromTagAPIView(GenericAPIView):
    """
    Detach a page from a tag.
    Only authorized users (owner or collaborators) can detach a page from a tag.
    """
    permission_classes = [IsAuthenticated, permissions.HasNoteInWorkspace, permissions.HasTagInWorkspace]
    serializer_class = TagAttachDetachSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():

            tag_id = serializer.validated_data.get("tag_id")
            note_id = serializer.validated_data.get("note_id")
            
            note = Note.objects.get(id=note_id)
            tag = Tag.objects.get(id=tag_id)
            
            self.check_object_permissions(request, note)
            self.check_object_permissions(request, tag)

            serializer.detach_tag_from_note()
            return standard_response(data={"message": "Tag detached successfully."}, status_code=status.HTTP_200_OK)
        return standard_response(errors=serializer.errors, is_success=False, status_code=status.HTTP_400_BAD_REQUEST)
