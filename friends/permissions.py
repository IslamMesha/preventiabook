from rest_framework import permissions


class IsMyFriendRequestOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, friend):
        return friend.from_user == request.user
