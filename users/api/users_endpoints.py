from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from users.pagination import MediumPage
from users.serializer import UserSerializer, UserSignUpSerializer, UserPasswordChangeSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from users.models import CustomUser
from rest_framework.filters import SearchFilter
from django.contrib.auth import authenticate
from django.utils.timezone import now
from plan.models import Plan, UserPlan

    
class GetUsersList(generics.ListAPIView):
    """
    List the users with pagination through this API.
    """    
    queryset = CustomUser.objects.filter(is_active=True)
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
            user_object = validated_data.save()
            
            return Response({"message": "User signed up"}, status=status.HTTP_201_CREATED)
        
        return Response({"message": validated_data.errors,}, status=status.HTTP_400_BAD_REQUEST)

class UpdataUser(generics.UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()
    parser_classes = [MultiPartParser, FormParser]
    lookup_field = 'email'

class DeleteAccount(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request):
        user = request.user
        CustomUser.objects.deactivate_user(user)

        return Response({"message": "User Deleted"})


class ChangePassword(APIView):
    permission_classes=[IsAuthenticated]
    serializer_class = UserPasswordChangeSerializer
    def post(self, request):
        user = request.user
        password = request.data["current_password"]
        if user.check_password(password):
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                new_password = serializer.validated_data.get("new_password")
                user.set_password(new_password)
                user.save()
                return Response({"message": "password changed succesfuly"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            
        else:
            return Response({"message": "Wrong password is provided"}, status=status.HTTP_401_UNAUTHORIZED)
