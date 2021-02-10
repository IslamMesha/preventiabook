from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from friends.models import FriendshipRequest, Friend
from friends.permissions import IsMyFriendRequestOrReadOnly
from friends.serializers import FriendshipRequestSerializer, FriendshipRequestUpdateSerializer, FriendSerializer


class FriendshipRequestViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing, send, accept and reject friend request.
    """
    serializer_class = FriendshipRequestSerializer
    queryset = FriendshipRequest.objects.order_by('-created')

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        decision = request.data.get('decision', 'View')
        instance = self.get_object()

        if decision == 'View':
            instance.mark_viewed()
        elif decision == 'Accept':
            instance.accept()
        elif decision == 'Reject':
            instance.reject()
        elif decision == 'Cancel':
            instance.cancel()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action in ('update',):
            return FriendshipRequestUpdateSerializer
        return self.serializer_class


class FriendViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for reading friends.
    """
    serializer_class = FriendSerializer
    queryset = Friend.objects.order_by('-created')
    permission_classes = (IsMyFriendRequestOrReadOnly, IsAuthenticated)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(to_user=request.user)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
