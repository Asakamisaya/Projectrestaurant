from rest_framework import serializers
from restaurant_app import models

class FoodmenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Foodmenu
        fields = '__all__'