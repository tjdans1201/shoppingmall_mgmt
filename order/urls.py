from django.urls import path
from .views import OrderAPI, update_pay_state,update_delivery_state


urlpatterns = [
    path("", OrderAPI.as_view()),
    path("/update/pay_state/<int:id>",update_pay_state),
    path("/update/delivery_state/<int:id>",update_delivery_state)
]