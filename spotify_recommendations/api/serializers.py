from django.contrib.auth.models import User, Group
from rest_framework import serializers

from spotify_recommendations.api.models import SanitizedNewRelease


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class NewReleaseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SanitizedNewRelease
        fields = ['release_name', 'artists', 'raw_response_id', 'url']