from django.contrib import admin

from social.models import Post, Comment, Like

admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Comment)
