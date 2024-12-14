from rest_framework import serializers
from workspace.models import Workspace, Folder
from .models import Note, Tag


class TagSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tag
        fields = ['id', 'name', 'description']
        read_only_fields = ['id']
        

class CreateTagSerializer(serializers.Serializer):
    workspace_id = serializers.IntegerField()
    name = serializers.CharField()
    description = serializers.CharField()
    
    def validate(self, data):
        workspace_id = data['workspace_id']
        if not Workspace.objects.filter(id=workspace_id).exists():
            raise serializers.ValidationError({"message": "workspace not found."})
        
        return data
    
    def create(self, validated_data):
        workspace_id = validated_data['workspace_id']
        
        workspace = Workspace.objects.get(id=workspace_id)
        
        tag = Tag.objects.create(workspace=workspace, description=validated_data["description"], name=validated_data["name"])

        return tag


class UpdateTagSerializer(serializers.ModelSerializer):
    
    id = serializers.IntegerField(required=True)
    
    class Meta:
        model = Tag
        fields = ['id', 'name', 'description']
    
    def validate_id(self, value):
        """
        Validate that the tag with the provided ID exists.
        """
        if not Tag.objects.filter(id=value).exists():
            raise serializers.ValidationError({"message": "Tag with the given ID does not exist."})
        return value 
        
    def update(self, instance, validated_data):
        
        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        instance.save()
        
        return instance


class TagAttachDetachSerializer(serializers.Serializer):
    tag_id = serializers.IntegerField(required=True)
    note_id = serializers.IntegerField(required=True)
    
    def validate_tag_id(self, value):
        """
        Validate that the tag exists.
        """
        try:
            tag = Tag.objects.get(id=value)
        except Tag.DoesNotExist:
            raise serializers.ValidationError("Tag with the given ID does not exist.")
        return value

    def validate_note_id(self, value):
        """
        Validate that the note exists.
        """
        try:
            note = Note.objects.get(id=value)
        except Note.DoesNotExist:
            raise serializers.ValidationError("Note with the given ID does not exist.")
        return value

    def attach_tag_to_note(self):
        """
        Attach the tag to the note.
        """
        tag = Tag.objects.get(id=self.validated_data['tag_id'])
        note = Note.objects.get(id=self.validated_data['note_id'])
        tag.notes.add(note)
        return tag

    def detach_tag_from_note(self):
        """
        Detach the tag from the note.
        """
        tag = Tag.objects.get(id=self.validated_data['tag_id'])
        note = Note.objects.get(id=self.validated_data['note_id'])
        tag.notes.remove(note)
        return tag



class AddNoteSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField(allow_null=True, required=False)
    workspace_id = serializers.IntegerField()
    folder_id = serializers.IntegerField(allow_null=True, required=False)
    
    def validate(self, data):
        workspace_id = data.get("workspace_id")
        if workspace_id is None:
            raise serializers.ValidationError({"message": "workspace_id is required."})
        
        if not Workspace.objects.filter(id=workspace_id).exists():
            raise serializers.ValidationError({"message": "didn't find workspace."})
        
        folder_id = data.get("folder_id", None)
        if folder_id:
            if not Folder.objects.filter(id=folder_id).exists():
                raise serializers.ValidationError({"message": "didn't find folder_id."})
        
        return data
    
    def create(self, validated_data):
        title = validated_data["title"]
        description = validated_data.get("description", None)
        workspace_id = validated_data.get("workspace_id")
        folder_id = validated_data.get("folder_id", None)

        workspace = Workspace.objects.get(id=workspace_id)
        if folder_id:
            folder = Folder.objects.get(id=folder_id)
            note = Note.objects.create(title=title, description=description, workspace=workspace, folder=folder)
            return note
        
        note = Note.objects.create(title=title, description=description, workspace=workspace)
        
        return note


class SaveNoteContentSerializer(serializers.Serializer):
    note_id = serializers.IntegerField(required=True)
    content = serializers.CharField(required=True)
    
    def validate_note_id(self, value):
        if not Note.objects.filter(id=value).exists():
            raise serializers.ValidationError("note_id not found.")
    
    def update(self, instance, validated_data):
        instance.content = validated_data.get("content", instance.content)
        instance.save()
        return instance

class NotesFilterSerializer(serializers.Serializer):
    workspace_id = serializers.IntegerField(required=True)
    note_title = serializers.CharField(required=False)
    tags = serializers.ListField(
        child = serializers.IntegerField(), required=False,
    )
    
    def validate_workspace_id(self, value):
        if not Workspace.objects.filter(id=value).exists():
            raise serializers.ValidationError("Workspace not found.")
        return value
    
    def validate_tags(self, value):
        workspace_id = self.initial_data.get('workspace_id')
        if workspace_id:
            valid_tag_ids = Tag.objects.filter(workspace_id=workspace_id).values_list('id', flat=True)
            invalid_tags = [tag_id for tag_id in value if tag_id not in valid_tag_ids]
            if invalid_tags:
                raise serializers.ValidationError(f"Invalid tag IDs: {', '.join(map(str, invalid_tags))}")
        return value
    

class NoteContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ["id", "title", "content", "created_at", "updated_at"]
    