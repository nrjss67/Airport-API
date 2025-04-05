from django.contrib import admin
from django.urls import include, path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from airport.permissions import ReadOnlyOrIsAdmin


schema_view = get_schema_view(
    openapi.Info(
        title="Airport Service API",
        default_version="v1",
        description="API for Airport Service",
        terms_of_service="#",
        contact=openapi.Contact(email="extazzzyprofit@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=False,
    permission_classes=(ReadOnlyOrIsAdmin,),
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/airport/", include("airport.urls", namespace="airport")),
    path("api/v1/user/", include("user.urls", namespace="user")),
    path(
        "api/v1/doc/swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]
