# Generated by Django 5.1.1 on 2024-09-10 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant_app', '0008_alter_foodmenu_description_alter_foodmenu_foodid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodmenu',
            name='foodid',
            field=models.AutoField(max_length=4, primary_key=True, serialize=False, verbose_name='Food_ID'),
        ),
    ]