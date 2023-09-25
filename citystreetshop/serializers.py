from rest_framework import serializers

from .models import City, Shop, Street


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"


class StreetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Street
        fields = "__all__"


class ShopSerializer(serializers.ModelSerializer):
    city = CitySerializer()
    street = StreetSerializer()

    class Meta:
        model = Shop
        fields = "__all__"

    def create(self, validated_data: dict):
        city_data = validated_data.pop("city")
        street_data = validated_data.pop("street")
        city, _ = City.objects.get_or_create(**city_data)
        street, _ = Street.objects.get_or_create(**street_data)
        return Shop.objects.create(city=city, street=street, **validated_data)
