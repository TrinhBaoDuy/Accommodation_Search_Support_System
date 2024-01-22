from django.core.exceptions import PermissionDenied
from rest_framework import permissions
from rest_framework.permissions import BasePermission


class CommentOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        if view.action == 'destroy':
            if request.user == obj.user or request.user == obj.post.user:
                return True
            else:
                print("You do not have permission to delete this comment.")
                return False
        elif view.action == 'change_value_comment':
            if request.user == obj.user:
                return True
            else:
                 print("You do not have permission to change the value of this comment.")
                 return False





