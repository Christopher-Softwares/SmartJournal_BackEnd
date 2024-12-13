from django.db import models
from workspace.models import Folder, Workspace


class Note(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    folder = models.ForeignKey(Folder, on_delete=models.SET_NULL, null=True, blank=True, related_name="notes")
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, null=False, blank=False, related_name="notes")

    def __str__(self):
        return self.title

        
class Tag(models.Model):
    """
    Tag model to categorize notes within a workspace.
    """
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    workspace = models.ForeignKey(Workspace, related_name="tags", on_delete=models.CASCADE)
    notes = models.ManyToManyField(Note, related_name="tags", blank=True)

    def __str__(self):
        return self.name
