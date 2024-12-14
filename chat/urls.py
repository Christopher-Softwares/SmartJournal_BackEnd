from rest_framework.urls import path
from chat.views import ListWorkspaceChats, NewPrompt


urlpatterns=[
    path("<int:workspace_id>/messages/", ListWorkspaceChats.as_view()),
    path('new_prompt/', NewPrompt.as_view(), name='new_prompt'),
]