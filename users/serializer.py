from rest_framework import serializers
from users.models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(required=False)
    class Meta:
        model = CustomUser
        fields = ['id', 'photo', 'bio', 'username', 'first_name', 'last_name', 'created_at', 'gender', 'age', 'country', 'city']
        read_only_fields = ['id']