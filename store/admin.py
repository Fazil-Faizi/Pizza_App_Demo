from django.contrib import admin
from .models import *

admin.site.register(Payment)
admin.site.register(Food)
admin.site.register(OrderFood)
admin.site.register(Order)
