from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.response import Response

from social.models import Post, Comment, Like


class AuthorRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password',)

    def create(self, validated_data):
        email = validated_data.get("email")
        password = validated_data.get("password")
        try:
            user, created = User.objects.get_or_create(email=email)
        except User.DoesNotExist:
            user = User.objects.create(email=email)
            user.username = email
            user.set_password(password)
            user.save()
            return user
        return user


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email',)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class CommentListSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'


class PostListSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = '__all__'

    @staticmethod
    def get_likes_count(post):
        return post.likes.count()


class AuthorStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('is_active',)
