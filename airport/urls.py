from django.urls import include, path
from rest_framework import routers

from .views import (
    CrewViewSet,
    AirplaneTypeViewSet,
    AirplaneViewSet,
    AirportViewSet,
    OrderViewSet,
    RouteViewSet,
    FlightViewSet,
    TicketViewSet,
)

router = routers.DefaultRouter()
router.register("crew", CrewViewSet)
router.register("airplane-type", AirplaneTypeViewSet)
router.register("airplane", AirplaneViewSet)
router.register("airport", AirportViewSet)
router.register("route", RouteViewSet)
router.register("flight", FlightViewSet)
router.register("ticket", TicketViewSet)
router.register("order", OrderViewSet)


urlpatterns = [
    path("", include(router.urls)),
]

app_name = "airport"
