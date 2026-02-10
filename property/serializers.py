from rest_framework import serializers
from .models import Location


class LocationAutocompleteSerializer(serializers.ModelSerializer):
    property_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Location
        fields = [
            "id",
            "name",
            "city",
            "country",
            "full_address",
            "property_count",
        ]
