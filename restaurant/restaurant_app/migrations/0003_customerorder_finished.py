# Generated by Django 5.1.1 on 2024-09-21 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant_app', '0002_customerorder_cooking_customerorder_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerorder',
            name='finished',
            field=models.BooleanField(default=False),
        ),
    ]