from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

AUTH_USER_MODEL = getattr(settings, "AUTH_USER_MODEL", "auth.User")


class FriendshipRequest(models.Model):
    """ Model to represent friendship requests """

    from_user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="friendship_requests_sent",
    )
    to_user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="friendship_requests_received",
    )

    message = models.TextField(_("Message"), blank=True)

    created = models.DateTimeField(default=timezone.now)
    rejected = models.DateTimeField(blank=True, null=True)
    viewed = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return "%s" % self.from_user_id

    def accept(self):
        """ Accept this friendship request """
        Friend.objects.get_or_create(from_user=self.from_user, to_user=self.to_user)

        Friend.objects.get_or_create(from_user=self.to_user, to_user=self.from_user)

        self.delete()

        # Delete any reverse requests
        FriendshipRequest.objects.filter(
            from_user=self.to_user, to_user=self.from_user
        ).delete()

    def reject(self):
        """ reject this friendship request """
        self.rejected = timezone.now()
        self.save()

    def mark_viewed(self):
        self.viewed = timezone.now()
        self.save()


class Friend(models.Model):
    """ Model to represent Friendships """

    to_user = models.ForeignKey(AUTH_USER_MODEL, models.CASCADE, related_name="friends")
    from_user = models.ForeignKey(
        AUTH_USER_MODEL, models.CASCADE, related_name="_unused_friend_relation"
    )
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "User #%s is friends with #%s" % (self.to_user_id, self.from_user_id)

    def save(self, *args, **kwargs):
        # Ensure users can't be friends with themselves
        if self.to_user == self.from_user:
            raise ValidationError("Users cannot be friends with themselves.")
        super(Friend, self).save(*args, **kwargs)
