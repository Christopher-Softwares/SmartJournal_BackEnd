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
from rag.chroma.chroma_collection import *
from rag.chroma.chroma_settings import ChromaDBConnectionSettings
from rag.rag_manager import RagManager
from rag.rag_settings import RagSettings
from django.conf import settings


class CreateNoteAPIView(StandardCreateAPIView):
    serializer_class = AddNoteSerializer
    permission_classes = [IsAuthenticated, permissions.IsWorkspaceOwnerOrMember]
    
    def perform_create(self, serializer):
        return serializer.save()
    
    def create(self, request, *args, **kwargs):
        workspace_id = request.data.get("workspace_id")
        workspace = Workspace.objects.filter(id=workspace_id)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        workspace_id = serializer.validated_data.get("workspace_id")
        workspace = Workspace.objects.get(id=workspace_id)
        
        self.check_object_permissions(request, workspace)
        
        note = self.perform_create(serializer)

        return standard_response(
            data={
                "note_id": note.id,
            },
            status_code=status.HTTP_201_CREATED
        )


class SaveNoteContentAPIView(StandardUpdateAPIView):
    serializer_class = SaveNoteContentSerializer
    permission_classes = [IsAuthenticated, permissions.HasNoteInWorkspace]
    
    def get_object(self):
        note_id = self.request.data.get("note_id")
        try:
            return Note.objects.get(id=note_id)
        except Note.DoesNotExist:
            return None
        
    def update(self, request, *args, **kwargs):
        note = self.get_object()
        
        self.check_object_permissions(request, note)
        
        if not note:
            return standard_response(
                errors = {"message": "Note with the given ID does not exist."},
                status_code=status.HTTP_404_NOT_FOUND,
                is_success=False,
            )

        serializer = self.get_serializer(note, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        try:
            chroma_settings = ChromaDBConnectionSettings(True, "https://christopher-smart-journal-chroma.liara.run/", 8000, "." + settings.MEDIA_URL + "chroma_db")
            rag_settings = RagSettings(
                openai_api_key = "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", 
                chunk_size = 400)

            connection_factory = ChromaDBConnectionFactory(settings= chroma_settings)

            collectionManager = ChromaCollectionManager(connection_factory)
            ragManager = RagManager(connection_factory, rag_settings)

            collectionManager.create_collection('wspace_' + str(note.workspace_id))
            ragManager.add_new_content(request.data['content'], collection_name = 'wspace_' +  str(note.workspace_id))
        except Exception as e:
            print(e.message)

        return standard_response(
            data={"message": "Note content updated successfully."},
            status_code=status.HTTP_200_OK,
        )


class FilterNotesView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, permissions.IsWorkspaceOwnerOrMember]
    serializer_class = NotesFilterSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        
        workspace_id = serializer.validated_data.get("workspace_id")
        note_title = serializer.validated_data.get("note_title", "")
        tags = serializer.validated_data.get("tags", [])
        
        workspace = Workspace.objects.get(id=workspace_id)
        
        # check workspace permission
        self.check_object_permissions(request, workspace)
        
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
    permission_classes = [IsAuthenticated, permissions.HasNoteInWorkspace]
    serializer_class = NoteContentSerializer
    
    def get_object(self):
        note_id = self.kwargs.get("note_id")
        note = get_object_or_404(Note, id=note_id)
        
        self.check_object_permissions(self.request, note)

        return note    
    