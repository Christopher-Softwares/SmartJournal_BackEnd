from django.urls import path, include
from users.views import *

urlpatterns = [
    path('users/all/', GetUsersListAPIView.as_view(), name='list_users'),
    path('me', GetAuthenticatedUser.as_view(), name="get_authenticated_user"),
    path('reset-password/', PasswordResetAPIView.as_view(), name="user_reset_password")
]