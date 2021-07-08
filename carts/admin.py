from carts.models import Cartiteam
from django.contrib import admin
from .models import Cart,Cartiteam

# Register your models here.
admin.site.register(Cart)
admin.site.register(Cartiteam)
