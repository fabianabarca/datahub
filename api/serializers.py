from feed.models import InfoService
from gtfs.models import *
from alerts.models import *
from rest_framework import serializers

# from gtfs.models import GTFSProvider, Route, Trip, StopTime, Stop, FeedInfo, Calendar, CalendarDate, Shape, GeoShape, FareAttribute, FareRule, ServiceAlert, Weather, Social, FeedMessage, TripUpdate, StopTimeUpdate, VehiclePosition, Record, Agency


class GTFSProviderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GTFSProvider
        fields = "__all__"


class NextTripSerializer(serializers.Serializer):
    
    stop_id = serializers.CharField()
    trip_id = serializers.CharField()


class AgencySerializer(serializers.HyperlinkedModelSerializer):

    feed = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Agency
        fields = "__all__"


class StopSerializer(serializers.HyperlinkedModelSerializer):

    feed = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Stop
        fields = "__all__"


class RouteSerializer(serializers.HyperlinkedModelSerializer):

    feed = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Route
        fields = "__all__"


class CalendarSerializer(serializers.HyperlinkedModelSerializer):

    feed = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Calendar
        fields = "__all__"


class CalendarDateSerializer(serializers.HyperlinkedModelSerializer):

    feed = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = CalendarDate
        fields = "__all__"


class ShapeSerializer(serializers.HyperlinkedModelSerializer):

    feed = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Shape
        fields = "__all__"


class GeoShapeSerializer(serializers.HyperlinkedModelSerializer):

    feed = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = GeoShape
        fields = "__all__"


class TripSerializer(serializers.HyperlinkedModelSerializer):

    feed = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Trip
        fields = "__all__"


class StopTimeSerializer(serializers.HyperlinkedModelSerializer):

    feed = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = StopTime
        fields = "__all__"


class FeedInfoSerializer(serializers.HyperlinkedModelSerializer):

    feed = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = FeedInfo
        fields = "__all__"


class FareAttributeSerializer(serializers.HyperlinkedModelSerializer):

    feed = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = FareAttribute
        fields = "__all__"


class FareRuleSerializer(serializers.HyperlinkedModelSerializer):

    feed = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = FareRule
        fields = "__all__"


class ServiceAlertSerializer(serializers.HyperlinkedModelSerializer):

    feed = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Alert
        fields = "__all__"


class WeatherSerializer(serializers.HyperlinkedModelSerializer):

    feed = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Weather
        fields = "__all__"


class SocialSerializer(serializers.HyperlinkedModelSerializer):

    feed = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Social
        fields = "__all__"


class FeedMessageSerializer(serializers.HyperlinkedModelSerializer):

    provider = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = FeedMessage
        fields = "__all__"


class TripUpdateSerializer(serializers.HyperlinkedModelSerializer):

    feed_message = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = TripUpdate
        fields = "__all__"


class StopTimeUpdateSerializer(serializers.HyperlinkedModelSerializer):

    trip_update = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = StopTimeUpdate
        fields = "__all__"


class VehiclePositionSerializer(serializers.HyperlinkedModelSerializer):

    feed_message = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = VehiclePosition
        fields = "__all__"


class RecordSerializer(serializers.HyperlinkedModelSerializer):

    provider = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Record
        fields = "__all__"


class InfoServiceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = InfoService
        fields = "__all__"
