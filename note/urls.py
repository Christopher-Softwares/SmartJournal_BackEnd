from django.urls import path, include

from .views import (
    # note apis
    CreateNoteAPIView,
    SaveNoteContentAPIView,
    FilterNotesView,
    GetNoteContent,

    # tag apis
    CreateTagAPIView,
    DeleteTagAPIView,
    UpdateTagAPIView,
    AttachPageToTagAPIView,
    DetachPageFromTagAPIView,
    GetWorkspaceTagsAPIView,
)

urlpatterns = [
    path("add/", CreateNoteAPIView.as_view(), name="create-note"),
    path("save_note/", SaveNoteContentAPIView.as_view(), name="save-note"),
    path("get_user_notes/", FilterNotesView.as_view(), name="filter-notes"),
    path("<int:note_id>/", GetNoteContent.as_view(), name="get-note-content"),

    # tag attach and detach
    path('tags/create/', CreateTagAPIView.as_view(), name='create-tag'),
    path('tags/<int:pk>/delete/', DeleteTagAPIView.as_view(), name='delete-tag'),
    path('tags/update/', UpdateTagAPIView.as_view(), name='update-tag'),
    path('add_tag_to_note/', AttachPageToTagAPIView.as_view(), name='attach-note-to-tag'),
    path('remove_tag_from_note/', DetachPageFromTagAPIView.as_view(), name='detach-note-from-tag'),
    path('get_workspace_tags/<int:workspace_id>/', GetWorkspaceTagsAPIView.as_view(), name='get-workspace-tags'),
]
