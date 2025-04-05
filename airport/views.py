from rest_framework import viewsets, mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import (
    Crew,
    AirplaneType,
    Airplane,
    Airport,
    Route,
    Flight,
    Order,
    Ticket,
)
from .serializers import (
    AirplaneCreateUpdateSerializer,
    AirplaneDetailSerializer,
    AirportDetailSerializer,
    CrewSerializer,
    AirplaneTypeSerializer,
    AirplaneSerializer,
    AirportSerializer,
    FlightCreateUpdateSerializer,
    FlightDetailSerializer,
    OrderSerializer,
    RouteCreateUpdateSerializer,
    RouteDetailSerializer,
    RouteSerializer,
    FlightSerializer,
    TicketPutUpdateSerializer,
    TicketSerializer,
)
from .permissions import OrderCreatePermission, ReadOnlyOrIsAdmin


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    permission_classes = (ReadOnlyOrIsAdmin,)
    authentication_classes = (JWTAuthentication,)


class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer
    permission_classes = (ReadOnlyOrIsAdmin,)
    authentication_classes = (JWTAuthentication,)


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer
    permission_classes = (ReadOnlyOrIsAdmin,)
    authentication_classes = (JWTAuthentication,)

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return AirplaneCreateUpdateSerializer
        if self.action == "retrieve":
            return AirplaneDetailSerializer
        return AirplaneSerializer

    def get_queryset(self):
        type = self.request.query_params.get("type")
        name = self.request.query_params.get("name")
        if type:
            return self.queryset.filter(airplane_type__name__icontains=type)
        if name:
            return self.queryset.filter(name__icontains=name)
        return self.queryset


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = (ReadOnlyOrIsAdmin,)
    authentication_classes = (JWTAuthentication,)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return AirportDetailSerializer
        return AirportSerializer

    def get_queryset(self):
        city = self.request.query_params.get("city")
        if city:
            return self.queryset.filter(closest_big_city__icontains=city)
        return self.queryset


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = (ReadOnlyOrIsAdmin,)
    authentication_classes = (JWTAuthentication,)

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return RouteCreateUpdateSerializer
        if self.action == "retrieve":
            return RouteDetailSerializer
        return RouteSerializer

    def get_queryset(self):
        source = self.request.query_params.get("source")
        destination = self.request.query_params.get("destination")
        if source:
            return self.queryset.filter(source__icontains=source)
        if destination:
            return self.queryset.filter(destination__icontains=destination)
        return self.queryset


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = (ReadOnlyOrIsAdmin,)
    authentication_classes = (JWTAuthentication,)

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return FlightCreateUpdateSerializer
        if self.action == "retrieve":
            return FlightDetailSerializer
        return FlightSerializer

    def get_queryset(self):
        source = self.request.query_params.get("source")
        destination = self.request.query_params.get("destination")
        departure_time = self.request.query_params.get("departure_time")
        arrival_time = self.request.query_params.get("arrival_time")
        if source:
            return self.queryset.filter(route__source__name__icontains=source)
        if destination:
            return self.queryset.filter(route__destination__name__icontains=destination)
        if departure_time:
            return self.queryset.filter(departure_time=departure_time)
        if arrival_time:
            return self.queryset.filter(arrival_time=arrival_time)
        return self.queryset


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    authentication_classes = (JWTAuthentication,)

    def get_queryset(self):
        created_at = self.request.query_params.get("created_at")
        if created_at:
            return self.queryset.filter(created_at=created_at)
        if self.request.user:
            return self.queryset.filter(user=self.request.user.id)
        return self.queryset

    def get_permissions(self):
        if self.action == "create":
            return (OrderCreatePermission(),)
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TicketViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):

    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()
    authentication_classes = (JWTAuthentication,)

    def get_queryset(self):
        source = self.request.query_params.get("source")
        destination = self.request.query_params.get("destination")
        departure_time = self.request.query_params.get("departure_time")
        arrival_time = self.request.query_params.get("arrival_time")

        if self.request.user:
            return self.queryset.filter(available=True)
        if source:
            return self.queryset.filter(flight__route__source__name__icontains=source)
        if destination:
            return self.queryset.filter(
                flight__route__destination__name__icontains=destination
            )
        if departure_time:
            return self.queryset.filter(flight__departure_time=departure_time)
        if arrival_time:
            return self.queryset.filter(flight__arrival_time=arrival_time)
        return self.queryset

    def get_serializer_class(self):
        if self.action in ("update", "partial_update"):
            return TicketPutUpdateSerializer
        return TicketSerializer

    def perform_create(self, serializer):
        ticket = serializer.save()
        ticket.avilable = False
        ticket.save()
