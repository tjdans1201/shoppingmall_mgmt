from django.urls import path
from .views import CouponsAPI

urlpatterns = [
    path("", CouponsAPI.as_view()),
]