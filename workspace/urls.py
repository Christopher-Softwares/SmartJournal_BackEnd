from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WorkspaceViewSet
from .views import (
    GetWorkspaceTagsAPIView,
    CreateTagAPIView,
    DeleteTagAPIView,
    UpdateTagAPIView,
    AttachPageToTagAPIView,
    DetachPageFromTagAPIView,
)


router = DefaultRouter()
router.register(r'workspaces', WorkspaceViewSet, basename='workspace')

urlpatterns = [
    path('', include(router.urls)),
    path('workspaces/<int:workspace_id>/tags/', GetWorkspaceTagsAPIView.as_view(), name='workspace-tags'),
    path('workspaces/<int:workspace_id>/tags/create/', CreateTagAPIView.as_view(), name='create-tag'),
    path('tags/<int:pk>/delete/', DeleteTagAPIView.as_view(), name='delete-tag'),
    path('tags/<int:pk>/update/', UpdateTagAPIView.as_view(), name='update-tag'),
    path('workspaces/<int:workspace_id>/tags/<int:tag_id>/pages/<int:page_id>/attach/', AttachPageToTagAPIView.as_view(), name='attach-page-to-tag'),
    path('workspaces/<int:workspace_id>/tags/<int:tag_id>/pages/<int:page_id>/detach/', DetachPageFromTagAPIView.as_view(), name='detach-page-from-tag'),
]
