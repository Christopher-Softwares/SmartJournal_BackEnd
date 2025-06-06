from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AddMembersToWorkspaceView,
    WorkspaceViewSet,
    RemoveMembersAPIView,
    GetOwnedWorkspaces,
    GetMemberWorkspaces,
    CreateFolderAPIView,
    UpdateFolderAPIView,
    DeleteFolderAPIView,
    UpdateFolderAPIView,
)

router = DefaultRouter()
router.register(r'workspaces', WorkspaceViewSet, basename='workspace')

urlpatterns = [
    path('workspaces/owned-by/', GetOwnedWorkspaces.as_view(), name='owned-workspaces'),
    path('workspaces/member-of/', GetMemberWorkspaces.as_view(), name='member-workspaces'),
    path('', include(router.urls)),
    path('workspaces/<int:workspace_id>/add_members/', AddMembersToWorkspaceView.as_view(), name='add-members'),
    path('workspaces/<int:workspace_id>/remove_members/', RemoveMembersAPIView.as_view(), name='remove-members'),

    # folder addresses
    path('folder/create/', CreateFolderAPIView.as_view(), name='create-folder'),
    path('folders/<int:pk>/delete/', DeleteFolderAPIView.as_view(), name='delete-folder'),
    path('folder/update/', UpdateFolderAPIView.as_view(), name='update-folder'),
 ]
