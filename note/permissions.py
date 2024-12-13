from rest_framework.permissions import BasePermission


class IsWorkspaceOwnerOrMember(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        workspace = obj.workspace
        
        return (
            workspace.owner == request.user or 
            workspace.members.filter(id=request.user.id).exists()
        )