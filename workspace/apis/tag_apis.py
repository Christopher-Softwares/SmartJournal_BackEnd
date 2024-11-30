from utils.response_wrapper import (
    StandardListAPIView, 
    StandardCreateAPIView,
    StandardDestroyAPIView,
    StandardUpdateAPIView,
    standard_response
) 
from django.shortcuts import get_object_or_404
from workspace.models import Workspace, Tag, Page
from workspace.serializers import TagSerializer
from workspace import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


class GetWorkspaceTagsAPIView(StandardListAPIView):
    """
    Retrieve all tags of a specific workspace.
    Only accessible to the workspace owner or collaborators.
    """
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        workspace_id = self.kwargs.get("workspace_id")
        workspace = get_object_or_404(Workspace, id=workspace_id)

        # Ensure the user is authorized to access the workspace
        self.check_object_permissions(self.request, workspace)

        # Return tags associated with the workspace
        return workspace.tags.all()
    
    
class CreateTagAPIView(StandardCreateAPIView):
    """
    Create a tag for a specific workspace.
    Only workspace owners or collaborators can create tags.
    """
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        workspace_id = self.kwargs.get("workspace_id")
        workspace = get_object_or_404(Workspace, id=workspace_id)

        serializer.save(workspace=workspace)


class DeleteTagAPIView(StandardDestroyAPIView):
    """
    Delete a specific tag.
    Only the owner of the workspace can delete tags.
    """
    queryset = Tag.objects.all()
    permission_classes = [IsAuthenticated]

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
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        tag = super().get_object()
        workspace = tag.workspace

        return tag

        

class AttachPageToTagAPIView(APIView):
    """
    Attach a page to a tag.
    Only authorized users (owner or collaborators) can attach a page to a tag.
    """
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated and authorized

    def post(self, request, workspace_id, tag_id, page_id, *args, **kwargs):
        # Retrieve the workspace, tag, and note
        workspace = get_object_or_404(Workspace, id=workspace_id)
        tag = get_object_or_404(Tag, id=tag_id, workspace=workspace)
        page = get_object_or_404(Page, id=page_id, workspace=workspace)

        # Attach the note to the tag
        tag.notes.add(note)

        return standard_response(data={"message": "Page successfully attached to tag."}, status_code=status.HTTP_200_OK, is_success=True)


class DetachPageFromTagAPIView(APIView):
    """
    Detach a page from a tag.
    Only authorized users (owner or collaborators) can detach a page from a tag.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, workspace_id, tag_id, page_id, *args, **kwargs):
        # Retrieve the workspace, tag, and note
        workspace = get_object_or_404(Workspace, id=workspace_id)
        tag = get_object_or_404(Tag, id=tag_id, workspace=workspace)
        page = get_object_or_404(Page, id=page_id, workspace=workspace)

        # Detach the page from the tag
        tag.notes.remove(page)

        return standard_response(data={"message": "Page successfully detached from tag."}, status_code=status.HTTP_200_OK, is_success=True)
