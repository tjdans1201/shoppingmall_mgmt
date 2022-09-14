from django.urls import path
from .views import CouponsAPI,CouponAPI

urlpatterns = [
    path("", CouponsAPI.as_view()),
    path("/<int:id>", CouponAPI.as_view())
]