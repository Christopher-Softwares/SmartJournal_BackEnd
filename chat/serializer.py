from rest_framework import serializers
from chat.models import Chat

class ChatSerializer(serializers.ModelSerializer):
    replied_to = serializers.SerializerMethodField()
    class Meta:
        model = Chat
        fields = ['id', 'message', 'order', 'msg_type', 'replied_to', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_parent(self, obj):
        if obj.replied_to:
            return ChatSerializer(obj.replied_to).data
        return None

class PromptSerializer(serializers.Serializer):
    workspace_id = serializers.IntegerField()
    prompt = serializers.CharField(max_length=1000)

    def validate_prompt(self, value):
        if len(str(value).strip()) == 0:
            raise serializers.ValidationError("Prompt message should not be empty")
        
        return value
