from ast import Del
from rest_framework import serializers
from .models import Delivery


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = [
            "quantity",
            "price",
            "buyr_city",
            "buyr_country",
            "buyr_zipx",
            "delivery_cost",
            "total_price",
        ]
