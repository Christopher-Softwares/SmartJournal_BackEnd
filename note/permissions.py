from rest_framework.permissions import BasePermission


class IsWorkspaceOwnerOrMember(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        # obj is workspace
        
        return (obj.owner == request.user or obj.members.filter(id=request.user.id).exists())


class HasNoteInWorkspace(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        # obj is note
        workspace = obj.workspace
        
        return (
            workspace.owner == request.user or 
            workspace.members.filter(id=request.user.id).exists()
        )