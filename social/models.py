from django.conf import settings
from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
        default=timezone.now, blank=True, null=True)
    published_date = models.DateTimeField(
        default=timezone.now, blank=True, null=True)
    attachment = models.FileField(
        upload_to='attachments/', blank=True, null=True)

    def number_of_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-published_date',)


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments', blank=False, null=False)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False, null=False)
    text = models.TextField(blank=False, null=False, default='')
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text


class Like(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='users')

    def __str__(self):
        return self.user.get_full_name() + ' likes ' + self.post.text
