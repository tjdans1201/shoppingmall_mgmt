from django.db import models

# Create your models here.
class CouponType(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=200)


class CouponCode(models.Model):
    id = models.AutoField(primary_key=True)
    coupon_type = models.ForeignKey(
        CouponType,
        related_name="couponcode_featured",
        on_delete=models.SET_NULL,
        null=True,
    )
    coupon_code = models.CharField(max_length=20, unique=True)
    amount = models.IntegerField()


class CouponHistory(models.Model):
    id = models.AutoField(primary_key=True)
    used_coupon = models.ForeignKey(CouponCode, on_delete=models.SET_NULL, null=True)
    discount_amount = models.FloatField()
