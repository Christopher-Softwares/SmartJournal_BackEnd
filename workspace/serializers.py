from rest_framework import serializers
from workspace.models import Workspace
from workspace.models import Folder
from django.contrib.auth.models import User
from users.serializer import UserSerializer
from rest_framework import serializers
from .models import Workspace
from django.contrib.auth import get_user_model

User = get_user_model()


class WorkspaceDetailSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True)
    class Meta:
        model = Workspace
        fields = '__all__'

class AddMembersSerializer(serializers.Serializer):
    member_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        help_text="List of user IDs to add to the workspace."
    )

    def validate_member_ids(self, value):
        # Ensure all users exist
        existing_users = User.objects.filter(id__in=value)
        if len(existing_users) != len(value):
            invalid_ids = set(value) - set(existing_users.values_list('id', flat=True))
            raise serializers.ValidationError(f"Invalid user IDs: {list(invalid_ids)}")
        return value

class RemoveMemberSerializer(serializers.Serializer):
    member_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        help_text="List of user IDs to remove from the workspace."
    )

    def validate(self, data):
        # Ensure the workspace exists in the context
        workspace = self.context.get('workspace')
        if not workspace:
            raise serializers.ValidationError("Workspace is required for member removal.")

        # Check if all members exist in the workspace
        invalid_members = [
            member_id for member_id in data['member_ids']
            if not workspace.members.filter(id=member_id).exists()
        ]

        if invalid_members:
            raise serializers.ValidationError(
                {"member_ids": f"Users with IDs {invalid_members} are not members of this workspace."}
            )
        return data




class CreateFolderSerializer(serializers.ModelSerializer):
    
    workspace_id = serializers.IntegerField(write_only=True)
    folder_name = serializers.CharField(max_length=255)
    
    class Meta:
        model = Folder
        fields = ["workspace_id", "folder_name"]
        
        
    def validate_workspace_id(self, value):
        if not Workspace.objects.filter(id=value).exists():
            raise serializers.ValidationError("Workspace with this ID does not exist.")
        return value
    
    
    def create(self, validated_data):
        folder_name = validated_data.pop("folder_name")
        workspace_id = validated_data.pop("workspace_id")

        data = {
            "title": folder_name,
            "workspace_id": workspace_id
        }

        folder = Folder.objects.create(**data)
        
        return folder


class UpdateFolderSerializer(serializers.ModelSerializer):
    folder_id = serializers.IntegerField()
    folder_name = serializers.CharField(max_length=255)
    
    class Meta:
        model = Folder
        fields = ["folder_id", "folder_name"]
