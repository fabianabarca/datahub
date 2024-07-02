from feed.models import Application
from gtfs.models import Provider
from rest_framework import serializers


class ApplicationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Application
        fields = ["url", "name", "description", "created_at", "updated_at"]


class ProviderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Provider
        fields = "__all__"