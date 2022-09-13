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
            "buyr_name"
        ]

class DeliveryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = [
            "id",
            "date",
            "pay_state",
            "quantity",
            "price",
            "delivery_cost",
            "total_price",
            "buyr_city",
            "buyr_country",
            "buyr_zipx",
            "delivery_num",
            "delivery_state",
            "buyr_name"
        ]

class DeliveryUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = ["pay_state","delivery_state"]