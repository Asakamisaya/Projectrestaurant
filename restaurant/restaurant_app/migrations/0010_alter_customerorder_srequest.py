# Generated by Django 5.1.2 on 2024-10-15 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant_app', '0009_customerorder_srequest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerorder',
            name='Srequest',
            field=models.CharField(blank=True, default=None, max_length=200, null=True, verbose_name='special request'),
        ),
    ]
