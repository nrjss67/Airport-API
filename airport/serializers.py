from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import (
    Crew,
    AirplaneType,
    Airplane,
    Airport,
    Route,
    Flight,
    Order,
    Ticket,
    User,
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "username", "email")


class CrewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name")


class AirplaneTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = AirplaneType
        fields = ("id", "name")


class AirplaneSerializer(serializers.ModelSerializer):
    airplane_type = serializers.SlugRelatedField("name", read_only=True)

    class Meta:
        model = Airplane
        fields = ("id", "name", "airplane_type")


class AirplaneCreateUpdateSerializer(AirplaneSerializer):
    airplane_type = serializers.PrimaryKeyRelatedField(
        queryset=AirplaneType.objects.all()
    )

    class Meta:
        model = Airplane
        fields = ("id", "name", "rows", "seats_in_row", "airplane_type")


class AirplaneDetailSerializer(AirplaneSerializer):
    total_seats = serializers.IntegerField(read_only=True)

    class Meta:
        model = Airplane
        fields = ("id", "name", "airplane_type", "rows", "seats_in_row", "total_seats")


class AirportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Airport
        fields = ("id", "name", "closest_big_city")


class AirportDetailSerializer(AirportSerializer):
    source_routes = serializers.SlugRelatedField(
        slug_field="name", read_only=True, many=True
    )
    destination_routes = serializers.SlugRelatedField(
        slug_field="name", read_only=True, many=True
    )

    class Meta:
        model = Airport
        fields = (
            "id",
            "name",
            "closest_big_city",
            "source_routes",
            "destination_routes",
        )


class RouteSerializer(serializers.ModelSerializer):
    destination = serializers.SlugRelatedField("name", read_only=True)
    source = serializers.SlugRelatedField("name", read_only=True)

    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")


class RouteCreateUpdateSerializer(RouteSerializer):
    destination = serializers.PrimaryKeyRelatedField(queryset=Airport.objects.all())
    source = serializers.PrimaryKeyRelatedField(queryset=Airport.objects.all())

    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")


class RouteDetailSerializer(RouteSerializer):
    destination = AirportSerializer(read_only=True)
    source = AirportSerializer(read_only=True)


class FlightSerializer(serializers.ModelSerializer):
    route = serializers.SlugRelatedField("short_name", read_only=True)
    airplane = serializers.SlugRelatedField("name", read_only=True)
    crew = serializers.SlugRelatedField("full_name", read_only=True, many=True)

    class Meta:
        model = Flight
        fields = ("id", "route", "airplane", "departure_time", "arrival_time", "crew")


class TicketSerializer(serializers.ModelSerializer):
    flight = FlightSerializer(read_only=True)
    order = serializers.SlugRelatedField(slug_field="id", read_only=True)

    class Meta:
        model = Ticket
        fields = (
            "id",
            "flight",
            "order",
            "row",
            "seat",
        )


class TicketAvailableSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = ("id", "row", "seat")


class TicketPutUpdateSerializer(TicketSerializer):
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())

    class Meta:
        model = Ticket
        fields = ("id", "order", "available")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["order"].queryset = Order.objects.filter(
            user=self.context["request"].user
        )


class FlightCreateUpdateSerializer(FlightSerializer):
    route = serializers.PrimaryKeyRelatedField(queryset=Route.objects.all())
    airplane = serializers.PrimaryKeyRelatedField(queryset=Airplane.objects.all())
    crew = serializers.PrimaryKeyRelatedField(queryset=Crew.objects.all(), many=True)

    class Meta:
        model = Flight
        fields = ("id", "route", "airplane", "departure_time", "arrival_time", "crew")


class FlightDetailSerializer(FlightSerializer):
    route = RouteDetailSerializer(read_only=True)
    airplane = AirplaneDetailSerializer(read_only=True)
    crew = CrewSerializer(read_only=True, many=True)
    available_tickets = TicketAvailableSerializer(read_only=True, many=True)

    class Meta:
        model = Flight
        fields = (
            "id",
            "route",
            "airplane",
            "departure_time",
            "arrival_time",
            "crew",
            "available_tickets",
        )


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    tickets = TicketSerializer(read_only=True, many=True)

    class Meta:
        model = Order
        fields = ("id", "created_at", "user", "tickets")
