from rest_framework import permissions
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress

class isAuthenticatedAndEmailVerified(permissions.BasePermission):
    ''' Custom permission to allow only verified users view a  route
     '''
    message = {
        "success": False,
        "message": "Your Email is not verified"
        }

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_verified)





