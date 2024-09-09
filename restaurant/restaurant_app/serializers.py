from rest_framework import serializers
from .models import Foodmenu

class FoodmenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Foodmenu
        fields = '__all__'