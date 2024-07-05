from feed.models import InfoService
from gtfs.models import GTFSProvider, Route, Trip
from rest_framework import serializers


class GTFSProviderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GTFSProvider
        fields = "__all__"


class InfoServiceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = InfoService
        fields = "__all__"


class RouteSerializer(serializers.HyperlinkedModelSerializer):

    feed = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Route
        fields = "__all__"


class TripSerializer(serializers.HyperlinkedModelSerializer):

    feed = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Trip
        fields = "__all__"
