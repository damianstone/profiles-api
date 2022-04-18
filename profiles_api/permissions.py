from rest_framework import permissions

class UpdateOwnProfile(permissions.BasePermission):
    
    """Allow user to edit their own profile"""
    
    # check user is trying to edit their own profile
    # every time that a request is made, django will call this function 
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        
        return obj.id == request.user.id


# Allow users to update their own status
class UpdateOwnStatus(permissions.BasePermission):
    # check the user is trying to update their own status
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.user_profile.id == request.user.id
   

    