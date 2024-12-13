from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from users.pagination import MediumPage
from users.serializer import UserSerializer, UserSignUpSerializer
from users.models import CustomUser
from rest_framework.filters import SearchFilter
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)
    
class GetUsersList(generics.ListAPIView):
    """
    List the users with pagination through this API.
    """    
    queryset = CustomUser.objects.all()
    permission_classes = [AllowAny]
    pagination_class = MediumPage
    serializer_class = UserSerializer
    filter_backends = [SearchFilter]
    search_fields =  ['email', 'first_name', 'last_name']
    

class GetAuthenticatedUser(generics.RetrieveAPIView):
    """
    Returns authenticated user
    """
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    
    def get_object(self):
        return self.request.user

class SingUp(generics.CreateAPIView):
    """
    User sign up api, email, password1, password2 is requiered
    """
    serializer_class = UserSignUpSerializer
    def post(self, request):
        signup_information = request.data
        validated_data = self.serializer_class(data=signup_information)
        if validated_data.is_valid():
            return Response({"message": "User signed up"}, status=status.HTTP_201_CREATED)
        
        return Response({"message": validated_data.errors,}, status=status.HTTP_400_BAD_REQUEST)

class UpdataUser(generics.UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

