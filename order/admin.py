from django.contrib import admin
from .models import Delivery, ContryCode, DeliveryCost

# Register your models here.
admin.site.register(Delivery)
admin.site.register(ContryCode)
admin.site.register(DeliveryCost)