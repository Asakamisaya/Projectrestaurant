# Generated by Django 5.1.2 on 2024-10-15 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant_app', '0008_employee_customerorder_foodname_customerorder_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerorder',
            name='Srequest',
            field=models.CharField(default=None, max_length=200, verbose_name='special request'),
        ),
    ]