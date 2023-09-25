import datetime

from django.db.models import QuerySet
from rest_framework import generics

from .models import City, Shop, Street
from .serializers import CitySerializer, ShopSerializer, StreetSerializer


class CityListAPIView(generics.ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class StreetListAPIView(generics.ListAPIView):
    queryset = Street.objects.all()
    serializer_class = StreetSerializer


class ShopCreateAPIView(generics.CreateAPIView):
    serializer_class = ShopSerializer


class ShopListAPIView(generics.ListAPIView):
    serializer_class = ShopSerializer

    def get_queryset(self) -> QuerySet:
        queryset = Shop.objects.all()
        street = self.request.query_params.get("street")
        city = self.request.query_params.get("city")
        if_open = self.request.query_params.get("open")

        if street:
            queryset = queryset.filter(street__name=street)
        if city:
            queryset = queryset.filter(city__name=city)
        if if_open:
            current_time = datetime.datetime.now(
                tz=datetime.timezone.utc,
            ).time()
            if if_open == "1":
                queryset = queryset.filter(
                    opening_time__lte=current_time,
                    closing_time__gte=current_time,
                )
            else:
                queryset = queryset.exclude(
                    opening_time__lte=current_time,
                    closing_time__gte=current_time,
                )

        return queryset
