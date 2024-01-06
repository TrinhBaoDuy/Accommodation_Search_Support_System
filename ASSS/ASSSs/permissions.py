from rest_framework import permissions


class CommentOwner(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, comment):
        if view.action == 'delete_comment':
            return request.user == comment.user or request.user == comment.post.user
        elif view.action == 'change_value_comment':
            return request.user == comment.user
