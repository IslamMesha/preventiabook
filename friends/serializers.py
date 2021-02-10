from rest_framework import serializers

from friends.models import FriendshipRequest, Friend
from social.serializers import AuthorSerializer

DECISION_CHOICES = (
    ('View', 'View'),
    ('Accept', 'Accept'),
    ('Reject', 'Reject'),
)


class FriendSerializer(serializers.ModelSerializer):
    to_user = AuthorSerializer()
    from_user = AuthorSerializer()

    class Meta:
        model = Friend
        fields = '__all__'


class FriendshipRequestSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = FriendshipRequest
        read_only_fields = ('created', 'viewed', 'rejected',)


class FriendshipRequestUpdateSerializer(serializers.ModelSerializer):
    decision = serializers.ChoiceField(choices=DECISION_CHOICES, required=False, write_only=True)

    class Meta:
        fields = '__all__'
        model = FriendshipRequest
        read_only_fields = ('created', 'viewed', 'rejected',)
