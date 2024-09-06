from django.contrib import admin

# Register your models here.
from .models import Foodmenu

class foofmenuadmin(admin.ModelAdmin):
    list_display = (' food_id','food_name','description','price')
# Register your models here.
admin.site.register(Foodmenu)