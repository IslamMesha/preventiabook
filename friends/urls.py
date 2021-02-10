from django.urls import path, include
from rest_framework.routers import DefaultRouter

from friends.views import FriendshipRequestViewSet, FriendViewSet

router = DefaultRouter()
router.register(r'friends', FriendViewSet)
router.register(r'requests', FriendshipRequestViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
