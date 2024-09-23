from django.contrib import admin

# Register your models here.
from .models import Foodmenu,Customerorder,Foodcategory,Receipt

class foofmenuadmin(admin.ModelAdmin):
    list_display = (' foodid','foodname','description','price')

class Customerorderadmin(admin.ModelAdmin):
    list_display = (' order_id','table_number','food','order_date','quantity')

class Foodcategoryadmin(admin.ModelAdmin):
    list_display = ('catename')

class Receiptadmin(admin.ModelAdmin):
    list_display = ('receipt_id', 'invoice', 'order', 'payment_method' ,'payment_amout' ,'recept_date')
# Register your models here.
admin.site.register(Foodmenu)
admin.site.register(Customerorder)
admin.site.register(Foodcategory)
admin.site.register(Receipt)