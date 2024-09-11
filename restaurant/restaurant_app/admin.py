from django.contrib import admin

# Register your models here.
from .models import Foodmenu,Customerorder

class foofmenuadmin(admin.ModelAdmin):
    list_display = (' foodid','foodname','description','price')

class Customerorderadmin(admin.ModelAdmin):
    list_display = (' order_id','table_number','food','order_date','quantity')
# Register your models here.
admin.site.register(Foodmenu)
admin.site.register(Customerorder)