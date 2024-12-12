from rest_framework import serializers
from users.models import CustomUser
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(required=False)
    class Meta:
        model = CustomUser
        fields = ['id', 'photo', 'bio', 'username', 'first_name', 'last_name', 'created_at', 'gender', 'age', 'country', 'city']
        read_only_fields = ['id']
        
class PasswordResetSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    new_password_repeat = serializers.CharField(write_only=True)
    
    def validate(self, data):
        user = self.context["request"].user
        
        if not user.check_password(data['old_password']):
            raise serializers.ValidationError({"message": "old password is incorrect."})
        
        if data["new_password"] != data["new_password_repeat"]:
            raise serializers.ValidationError({"message": "new_password and new_password_repeat don't match."})
        
        return data
    
    def save(self):      
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user
