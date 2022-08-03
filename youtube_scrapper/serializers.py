from rest_framework import serializers
from .models import Products


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ('id', 'code', 'type', 'availability', 'needing_repair', 'durability', 'max_durability', 'mileage', 'minimum_rent_period')
