from utils.response_wrapper import (
    standard_response,
    StandardCreateAPIView,
    StandardUpdateAPIView,
    StandardRetrieveAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, generics
from note.serializers import AddNoteSerializer, SaveNoteContentSerializer, NotesFilterSerializer, NoteContentSerializer
from note.models import Note
from note import permissions
from workspace.models import Workspace, Folder
from django.shortcuts import get_object_or_404


class CreateNoteAPIView(StandardCreateAPIView):
    serializer_class = AddNoteSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        return serializer.save()
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        note = self.perform_create(serializer)

        return standard_response(
            data={
                "note_id": note.id,
            },
            status_code=status.HTTP_201_CREATED
        )


class SaveNoteContentAPIView(StandardUpdateAPIView):
    serializer_class = SaveNoteContentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        note_id = self.request.data.get("note_id")
        try:
            return Note.objects.get(id=note_id)
        except Note.DoesNotExist:
            return None
        
    def update(self, request, *args, **kwargs):
        note = self.get_object()
        if not note:
            return standard_response(
                errors = {"message": "Note with the given ID does not exist."},
                status_code=status.HTTP_404_NOT_FOUND,
                is_success=False,
            )

        serializer = self.get_serializer(note, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return standard_response(
            data={"message": "Note content updated successfully."},
            status_code=status.HTTP_200_OK,
        )


class FilterNotesView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotesFilterSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        
        workspace_id = serializer.validated_data.get("workspace_id")
        note_title = serializer.validated_data.get("note_title", "")
        tags = serializer.validated_data.get("tags", [])
        
        workspace = Workspace.objects.get(id=workspace_id)
        
        notes_query = Note.objects.filter(workspace=workspace)
        
        if note_title:
            notes_query = notes_query.filter(title__icontains=note_title)
            
        if tags:
            notes_query = notes_query.filter(tags__id__in=tags)
            
        notes_with_folder = notes_query.filter(folder__isnull=False)
        notes_without_folder = notes_query.filter(folder__isnull=True)
        
        folders = []
        
        for folder in Folder.objects.filter(workspace=workspace):
            folder_notes = notes_with_folder.filter(folder=folder).all()
            
            if folder_notes.exists():
                folders.append(
                    {
                        "folder_id": folder.id,
                        "title": folder.title,
                        "notes": [{
                            "note_id": note.id,
                            "title": note.title,
                            "description": note.description,
                            "created_data": note.created_at,
                            } for note in folder_notes]
                    }
                )
        
        notes = [{
            "note_id": note.id,
            "title": note.title,
            "description": note.description,
            "created_date": note.created_at
            } for note in notes_without_folder]
        
        response_data = {
            
        }
        return standard_response(
            data={
                "notes": notes,
                "folders": folders,
            },
            is_success=True,
            status_code=status.HTTP_200_OK,
        )
        
class GetNoteContent(StandardRetrieveAPIView):
    permission_classes = [IsAuthenticated, permissions.IsWorkspaceOwnerOrMember]
    serializer_class = NoteContentSerializer
    
    def get_object(self):
        note_id = self.kwargs.get("note_id")
        note = get_object_or_404(Note, id=note_id)
        
        self.check_object_permissions(self.request, note)

        return note    
    