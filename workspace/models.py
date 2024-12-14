from django.db import models
from django.conf import settings
import uuid


class Workspace(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ownedworkspaces")
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="workspaces")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_active = models.DateTimeField(auto_now=True)
    is_archived = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name


class Folder(models.Model):
    """
    Each folder has multiple notes in it
    """
    title = models.CharField(max_length=255)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, null=False, blank=False)
    
    def __str__(self):
        return self.title
