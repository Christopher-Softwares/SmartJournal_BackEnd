from rest_framework import serializers
from workspace.models import Workspace
from workspace.models import Page
from django.contrib.auth.models import User
from users.serializer import UserSerializer


class WorkspaceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = ['id', 'name', 'description']
        read_only_fields = ["owner"]

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)

class PageSerializer():
    class Meta:
        model = Page
        fields = ['id', 'title']
        read_only_fields = ['id']

class WorkspaceDetailSerializer(serializers.ModelSerializer):
    members = UserSerializer()
    pages = PageSerializer()
    class Meta:
        model = Workspace
        fields = '__all__'

class AddMemberSerializer(serializers.Serializer):
    member_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True)

    def update(self, instance, validated_data):
        member_ids = validated_data['member_ids']
        members_to_add = User.objects.filter(id__in=member_ids)
        instance.members.add(*members_to_add)
        instance.save()
        return instance

class RemoveMemberSerializer(serializers.Serializer):
    member_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True)

    def update(self, instance, validated_data):
        member_ids = validated_data['member_ids']
        members_to_remove = User.objects.filter(id__in=member_ids)
        instance.members.remove(*members_to_remove)
        instance.save()
        return instance

class AddPageSerializer(serializers.Serializer):
    page_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True)

    def update(self, instance, validated_data):
        page_ids = validated_data['page_ids']
        pages_to_add = Page.objects.filter(id__in=page_ids)
        instance.pages.add(*pages_to_add)
        instance.save()
        return instance

class RemovePageSerializer(serializers.Serializer):
    page_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True)

    def update(self, instance, validated_data):
        page_ids = validated_data['page_ids']
        pages_to_remove = Page.objects.filter(id__in=page_ids)
        instance.pages.remove(*pages_to_remove)
        instance.save()
        return instance
