import os.path
from importlib.resources import files
from lib2to3.fixes.fix_input import context

from PIL.ImageOps import posterize
from django.contrib.auth.models import update_last_login
from django.core.files.storage import FileSystemStorage
from django.core.signals import request_started
from django.db.models import Max
from django.shortcuts import render, redirect
from django import forms
from .models import Foodmenu
from .serializers import FoodmenuSerializer
from restaurant_app import models
from rest_framework import viewsets, mixins

from restaurant import settings


# Create your views here.

class foodmenuView(viewsets.ModelViewSet):
    serializer_class = FoodmenuSerializer
    def get_queryset(self):
        return Foodmenu.objects.all()


def menulist(request):
    queryset = models.Foodmenu.objects.all()
    return render(request,'MenuAdmin.html',{'queryset':queryset})



class addmenuform(forms.ModelForm):
    class Meta:
        model = Foodmenu
        fields = "__all__"


def addtomenu(request):

    if request.method == 'GET':
        form = addmenuform()
        return render(request, 'addmenu.html', {"form":form})

    if request.method == 'GET':
       # foodname = request.POST['foodname']
       # description = request.POST['description']
       # price =request.POST['price']
       # img = request.FILES['img']

        #save = models.Foodmenu(foodname=foodname, description=description, price=price, img=img)
        #save.save(update_fields=['enable'])
        #print(save.errors)
        #return redirect('/')

        form = addmenuform(data=request.POST)
        print(form.errors)
        form.save()
        return redirect('addmenu.html')

    return redirect('/')

