from django.urls import path

from .views import (
    CityListAPIView,
    ShopCreateAPIView,
    ShopListAPIView,
    StreetListAPIView,
)

urlpatterns = [
    path("city/", CityListAPIView.as_view(), name="city-list"),
    path("city/street/", StreetListAPIView.as_view(), name="street-list"),
    path("shop/", ShopCreateAPIView.as_view(), name="shop-create"),
    path("shop/list/", ShopListAPIView.as_view(), name="shop-list"),
]
