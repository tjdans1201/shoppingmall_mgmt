from ast import Del
from rest_framework import serializers
from .models import CouponCode


class CouponCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CouponCode
        fields = [
            "coupon_type",
            "coupon_code",
            "amount",
        ]