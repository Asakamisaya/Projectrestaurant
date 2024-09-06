from django.db import models

# Create your models here.
class Foodmenu(models.Model):
    food_id = models.CharField(verbose_name='Food_ID', primary_key=True, max_length=4)
    food_name = models.CharField(verbose_name='Food_Name', max_length=50)
    description = models.CharField(verbose_name='Description', max_length=255)
    price = models.DecimalField(verbose_name='Price', max_digits=10, decimal_places=2)
    img = models.ImageField(db_column='Img', upload_to='images/',verbose_name = 'food image')