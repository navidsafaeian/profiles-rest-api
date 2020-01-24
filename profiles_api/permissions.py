from rest_framework import permissions

class UpdateOwnProfile(permissions.BasePermission):
    '''Allow user to edit their own profile'''

    def has_object_permission(self, request, view, obj):
        '''chack user is trying to edit their own profile'''
        # safe method is the method does not require any change in object, like GET method
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.id == request.user.id

