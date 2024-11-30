from django.urls import path, include
from users.views import *

urlpatterns = [
    path('users/all/', GetUsersListAPIView.as_view(), name='list_users'),
    path('users/me', GetAuthenticatedUser.as_view(), name="get_authenticated_user")
]