from rest_framework import serializers
from workspace.models import Workspace
from workspace.models import Folder
from django.contrib.auth.models import User
from users.serializer import UserSerializer
from rest_framework import serializers
from .models import Workspace
from django.contrib.auth import get_user_model


User = get_user_model()

class WorkspaceSerializer(serializers.ModelSerializer):
    members = serializers.SlugRelatedField(queryset=User.objects.all(), many=True, slug_field='email')
    class Meta:
        model = Workspace
        fields = '__all__'
        read_only_fields = ["created_at", "updated_at", "last_active"]

    def validate(self, attrs):
        request = self.context.get("request")
        user_plan = getattr(request.user, 'user_plan', None)
        
        if not user_plan:
            raise serializers.ValidationError(
                {"message": "User does not have a default plan"}
            )
        
        if not user_plan.can_add_workspace:
            raise serializers.ValidationError(
                {"message": "Exceeded workspace count limit for your plan"}
            )
    
        return attrs

class AddMembersSerializer(serializers.Serializer):
    member_emails = serializers.ListField(
        child=serializers.EmailField(),
        write_only=True,
        help_text="List of user emails to add to the workspace."
    )

    def validate_member_emails(self, value):
        existing_users = User.objects.filter(email__in=value)
        if len(existing_users) != len(value):
            invalid_emails = set(value) - set(existing_users.values_list('id', flat=True))
            raise serializers.ValidationError(f"Invalid user emails: {list(invalid_emails)}")
        return value

class RemoveMemberSerializer(serializers.Serializer):
    member_emails = serializers.SlugRelatedField(queryset=User.objects.all(), many=True, slug_field='email')

    def validate(self, data):
        workspace = self.context.get('workspace')
        if not workspace:
            raise serializers.ValidationError("Workspace is required for member removal.")
        
        invalid_members = [
            member_email for member_email in data['member_emails']
            if not workspace.members.filter(email=member_email).exists()
        ]
        print(invalid_members)

        if invalid_members:
            raise serializers.ValidationError(
                {"member_emails": f"Users with emails {invalid_members} are not members of this workspace."}
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
