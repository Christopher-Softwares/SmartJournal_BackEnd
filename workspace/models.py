from django.db import models
from django.conf import settings
import uuid


class Workspace(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ownedworkspaces")
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="workspaces")
    
    pages = models.ManyToManyField("Page", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_active = models.DateTimeField(auto_now=True)
    is_archived = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name


class Folder(models.Model):
    """
    Each folder has multiple Pages in it
    """
    title = models.CharField(max_length=255)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, null=False, blank=False)
    
    def __str__(self):
        return self.name


class Page(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    folder = models.ForeignKey(Folder, on_delete=models.SET_NULL, null=True, blank=True, related_name="pages")

    def __str__(self):
        return self.title


class Tag(models.Model):
    """
    Tag model to categorize pages within a workspace.
    """
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    workspace = models.ForeignKey(Workspace, related_name="tags", on_delete=models.CASCADE)
    pages = models.ManyToManyField(Page, related_name="tags", blank=True)

    def __str__(self):
        return self.name

