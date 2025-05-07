from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("json_test/", views.json_test, name="json_test"),
    path("listings/", views.get_all_listings, name="get_all_listings"),
    path(
        "listings/<str:zillow_str>/",
        views.get_listing_by_zillow_id,
        name="get_listing_by_zillow_id",
    ),
    path("query/", views.query, name="query"),
]
