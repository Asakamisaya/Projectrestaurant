from django.contrib import admin

# Register your models here.
from .models import Foodmenu, Customerorder, Foodcategory, Receipt, Foodcategory, Entertokens


class foofmenuadmin(admin.ModelAdmin):
    list_display = (' foodid','foodname','description','price')

class Customerorderadmin(admin.ModelAdmin):
    list_display = (' order_id','table_number','food','foodname','price','Srequest','order_date','quantity')

class Foodcategoryadmin(admin.ModelAdmin):
    list_display = ('catename')

class Receiptadmin(admin.ModelAdmin):
    list_display = ('receipt_id', 'invoice', 'order', 'payment_method' ,'payment_amout' ,'recept_date')

class Tokenadmin(admin.ModelAdmin):
    list_display = ('Token')

# Register your models here.
admin.site.register(Foodmenu)
admin.site.register(Customerorder)
admin.site.register(Foodcategory)
admin.site.register(Receipt)
admin.site.register(Entertokens)