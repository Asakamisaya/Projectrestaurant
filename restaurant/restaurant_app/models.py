from django.db import models

# Create your models here.
class Foodmenu(models.Model):
    foodid = models.AutoField(verbose_name='Food_ID', primary_key=True)
    foodname = models.CharField(verbose_name='Food_Name', max_length=50,default=None)
    description = models.CharField(verbose_name='Description', max_length=255,default=None)
    price = models.DecimalField(verbose_name='Price', max_digits=10, decimal_places=2,default=None)
    img = models.ImageField(db_column='Img', upload_to='images/',verbose_name = 'food image',default=None)

    class Meta:
        ordering = ['foodid']

    def __str__(self):
        return self.foodname

class Customerorder(models.Model):
    order_id = models.CharField(db_column='Order_ID', primary_key=True, max_length=5)  # Field name made lowercase.
    table_number = models.CharField(db_column='Table_Number', max_length=5)  # Field name made lowercase.
    food = models.ForeignKey(to='Foodmenu',on_delete=models.CASCADE,db_column='Food_ID')  # Field name made lowercase.
    order_date = models.DateField(db_column='Order_Date')  # Field name made lowercase.
    quantity = models.IntegerField(db_column='Quantity')


    def __str__(self):
        return self.order_id + '  ' + self.table_number+ '  '