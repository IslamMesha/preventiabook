from django.contrib import admin

from friends.models import FriendshipRequest, Friend

admin.site.register(Friend)
admin.site.register(FriendshipRequest)
