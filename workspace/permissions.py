from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to only allow owners of an object to edit or delete it.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        
        return obj.user == request.user

class IsMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user in obj.members:
            return True
        
        return  False


class IsWorkspaceOwnerOrMember(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        # obj is workspace
        
        return (obj.owner == request.user or obj.members.filter(id=request.user.id).exists())
