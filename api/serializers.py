from feed.models import Application
from rest_framework import serializers


class ApplicationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Application
        fields = ["url", "name", "description", "created_at", "updated_at"]
