from django.shortcuts import render
from .serializers import FoodmenuSerializer
from .models import Foodmenu
from rest_framework import viewsets, mixins

# Create your views here.

class foodmenuView(viewsets.ModelViewSet):
    serializer_class = FoodmenuSerializer
    def get_queryset(self):
        return Foodmenu.objects.all()