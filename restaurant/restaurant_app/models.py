from django.db import models

# Create your models here.

class Foodcategory(models.Model):
    catename = models.CharField(verbose_name='Category', primary_key=True,max_length=50,default=None)

    def __str__(self):
        return self.catename



class Foodmenu(models.Model):
    foodid = models.AutoField(verbose_name='Food_ID', primary_key=True)
    foodname = models.CharField(verbose_name='Food Name', max_length=50,default=None)
    description = models.CharField(verbose_name='Description', max_length=255,default=None)
    price = models.DecimalField(verbose_name='Price', max_digits=10, decimal_places=2,default=None)
    img = models.ImageField(upload_to='images/',verbose_name = 'img',default=None, null=True, blank=True)
    catename = models.ForeignKey(to='Foodcategory', on_delete=models.SET_NULL, verbose_name='Category Name',null=True, blank=True)
    deleted = models.BooleanField(default=False)
    soldout = models.BooleanField(default=False)


    class Meta:
        ordering = ['foodid']

    def __str__(self):
        return self.foodname

class Customerorder(models.Model):
    logid = models.AutoField(primary_key=True)
    order_id = models.CharField(verbose_name='Order_ID',max_length=5,default=None)
    table_number = models.CharField(verbose_name='Table_Number', max_length=5)
    food = models.CharField(verbose_name='Food_ID', max_length=5)
    order_date = models.DateField(verbose_name='Order_Date')  # Field name made lowercase.
    quantity = models.IntegerField(verbose_name='Quantity')
    cancled =  models.BooleanField(default=False)
    cooking = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)



    class Meta:
        ordering = ['order_id']


    def __str__(self):
        return self.order_id




