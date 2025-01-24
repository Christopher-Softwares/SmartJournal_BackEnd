from django.urls import path, include
from users.views import *

urlpatterns = [
    path('all/', GetUsersList.as_view(), name='list_users'),
    path('me/', GetAuthenticatedUser.as_view(), name="get_authenticated_user"),
    path('signup/', SingUp.as_view(), name='signup'),
    path('complete_info/<str:email>/', UpdataUser.as_view(), name='complete_information'),
    path('delete_account/', DeleteAccount.as_view(), name='delete_account'),
    path('change_password/', ChangePassword.as_view(), name='change_password')
]