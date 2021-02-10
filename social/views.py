from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from social.models import Post, Comment, Like
from social.permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly
from social.serializers import PostSerializer, PostListSerializer, CommentSerializer, CommentListSerializer, \
    LikeSerializer, AuthorStatusSerializer, AuthorSerializer, AuthorRegisterSerializer


class Registration(CreateAPIView):
    """
    A simple view to register new users.
    """
    serializer_class = AuthorRegisterSerializer


class LogAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('user')
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'created': created,
            'user_id': user.pk,
            'email': user.email
        })


class CommentViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing comments.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def list(self, request, *args, **kwargs):
        post_id = request.GET.get('post_id')
        if post_id:
            self.queryset = self.queryset.filter(post__id=post_id)

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = CommentListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = CommentListSerializer(queryset, many=True)
        return Response({'comments': serializer.data})

    def get_permissions(self):
        if self.action not in ('list', 'retrieve',):
            for permission in (IsOwnerOrReadOnly, IsAdminOrReadOnly,):
                self.permission_classes.append(permission)
        return [permission() for permission in self.permission_classes]


class PostViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing posts.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    def list(self, request, *args, **kwargs):
        author_id = request.GET.get('author_id')
        order_by = request.GET.get('order_by', 'Old')
        if author_id:
            self.queryset = self.queryset.filter(author__id=author_id)
        if order_by == 'Old':
            # Post are sorted by new as default.
            self.queryset = self.queryset.order_by('published_date')

        page = self.paginate_queryset(self.queryset)
        if page is not None:
            serializer = PostListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response({'posts': PostListSerializer(self.queryset, many=True).data})

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = PostListSerializer(instance)
        return Response(serializer.data)

    def get_permissions(self):
        if self.action not in ('list', 'retrieve',):
            for permission in (IsOwnerOrReadOnly, IsAdminOrReadOnly,):
                self.permission_classes.append(permission)
        return [permission() for permission in self.permission_classes]


class LikeViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet to like and dislike posts.
    """
    queryset = Like.objects.all()
    serializer_class = LikeSerializer


class AccountViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing, activating and deactivating accounts (Users).
    """
    permission_classes = (IsAdminUser,)
    serializer_class = AuthorStatusSerializer
    queryset = User.objects.order_by('-date_joined')

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve',):
            return AuthorSerializer
        return self.serializer_class
