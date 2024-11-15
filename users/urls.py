from django.urls import path, include
from users.views import *

urlpatterns = [
    path('users/all/', GetUsersListAPIView.as_view(), name='list_users'),
    path('users/<int:id>/', GetUserByIdAPIView.as_view(), name='user_detail_by_id')
]