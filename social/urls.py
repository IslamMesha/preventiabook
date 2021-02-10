from django.urls import path, include
from rest_framework.routers import DefaultRouter

from social.views import LogAuthToken, PostViewSet, CommentViewSet, LikeViewSet, AccountViewSet, Registration

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'likes', LikeViewSet)
router.register(r'users', AccountViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LogAuthToken.as_view()),
    path('register/', Registration.as_view()),
]
