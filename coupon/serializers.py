from dataclasses import fields
from rest_framework import serializers
from .models import CouponCode, CouponHistory, CouponType


class CouponCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CouponCode
        fields = [
            "coupon_type",
            "coupon_code",
            "amount",
        ]

class CouponHistoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CouponHistory
        fields = ["used_coupon", "discount_amount"]

