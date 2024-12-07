from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DeleteTagAPIView,
    UpdateTagAPIView,
    AttachPageToTagAPIView,
    DetachPageFromTagAPIView,
    AddMembersToWorkspaceView,
    WorkspaceViewSet,
    RemoveMembersAPIView,
    GetOwnedWorkspaces,
    GetMemberWorkspaces
)

router = DefaultRouter()
router.register(r'workspaces', WorkspaceViewSet, basename='workspace')

urlpatterns = [
    path('workspaces/owned-by/', GetOwnedWorkspaces.as_view(), name='owned-workspaces'),
    path('workspaces/member-of/', GetMemberWorkspaces.as_view(), name='member-workspaces'),
    path('', include(router.urls)),
    path('workspaces/<int:workspace_id>/add_members/', AddMembersToWorkspaceView.as_view(), name='add-members'),
    path('workspaces/<int:workspace_id>/remove_members/', RemoveMembersAPIView.as_view(), name='remove-members'),
    path('tags/<int:pk>/delete/', DeleteTagAPIView.as_view(), name='delete-tag'),
    path('tags/<int:pk>/update/', UpdateTagAPIView.as_view(), name='update-tag'),
    path('workspaces/<int:workspace_id>/tags/<int:tag_id>/pages/<int:page_id>/attach/', AttachPageToTagAPIView.as_view(), name='attach-page-to-tag'),
    path('workspaces/<int:workspace_id>/tags/<int:tag_id>/pages/<int:page_id>/detach/', DetachPageFromTagAPIView.as_view(), name='detach-page-from-tag'),
]
