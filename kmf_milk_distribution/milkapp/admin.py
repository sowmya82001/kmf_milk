# admin.py
from django.contrib import admin
from .models import MilkProduction, NandiniShop, Vehicle, DeliverySchedule, Order, QualityControl, MilkVariant, PricingStrategy

admin.site.register(MilkProduction)
admin.site.register(NandiniShop)
admin.site.register(Vehicle)
admin.site.register(DeliverySchedule)
admin.site.register(Order)
admin.site.register(QualityControl)
admin.site.register(MilkVariant)
admin.site.register(PricingStrategy)
