from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import City, Shop, Street
from .serializers import CitySerializer, ShopSerializer, StreetSerializer


class CityStreetShopTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.city1 = City.objects.create(name="City 1")
        self.city2 = City.objects.create(name="City 2")
        self.street1 = Street.objects.create(name="Street 1", city=self.city1)
        self.street2 = Street.objects.create(name="Street 2", city=self.city2)
        self.shop1 = Shop.objects.create(
            name="Shop 1",
            city=self.city1,
            street=self.street1,
            house="123",
            opening_time="00:00",
            closing_time="23:59",
        )
        self.shop2 = Shop.objects.create(
            name="Shop 2",
            city=self.city2,
            street=self.street2,
            house="456",
            opening_time="08:00",
            closing_time="17:30",
        )

    def test_get_all_cities(self):
        url = reverse("city-list")
        response = self.client.get(url)
        cities = City.objects.all()
        serializer_data = CitySerializer(cities, many=True).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer_data)

    def test_get_all_streets_of_city(self):
        url = reverse("street-list")
        response = self.client.get(url)
        streets = Street.objects.all()
        serializer_data = StreetSerializer(streets, many=True).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer_data)

    def test_create_shop(self):
        url = reverse("shop-create")

        data = {
            "name": "New Shop",
            "city": {
                "name": self.city1.name,
            },
            "street": {
                "name": self.street1.name,
                "city": self.street1.city.id,
            },
            "house": "789",
            "opening_time": "10:00",
            "closing_time": "19:00",
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Shop.objects.count(), 3)

    def test_get_all_shops(self):
        url = reverse("shop-list")
        response = self.client.get(url)
        shops = Shop.objects.all()
        serializer_data = ShopSerializer(shops, many=True).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer_data)

    def test_get_filtered_shops(self):
        url = reverse("shop-list")
        query_params = {"street": self.street1.name, "open": "1"}

        response = self.client.get(url, query_params)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], self.shop1.id)
