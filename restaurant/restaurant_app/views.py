import os.path
from idlelib.rpc import request_queue
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
    queryset = models.Foodmenu.objects.filter(deleted=False)
    return render(request,'MenuAdmin.html',{'queryset':queryset})



class addmenuform(forms.ModelForm):
    class Meta:
        model = Foodmenu
        # fields = "__all__"
        # exclude = ('foodid',)
        fields = ['foodname', 'description', 'price', 'img']

    def __init__(self, *args, **kwargs):
        super(addmenuform, self).__init__(*args, **kwargs)
        self.fields['img'].required = False
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control","placeholder": field.label}

class edititemform(forms.ModelForm):
    class Meta:
        model = Foodmenu
        # fields = "__all__"
        # exclude = ('foodid',)
        fields = ['foodname', 'description', 'price', 'img']

    def __init__(self, *args, **kwargs):
        super(edititemform, self).__init__(*args, **kwargs)
        #self.fields['img'].required = False
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control","placeholder": field.label}



def addtomenu(request):

    if request.method == 'GET':
        form = addmenuform()
        return render(request, 'addmenu.html', {"form":form})

    if request.method == 'POST':

        form = addmenuform(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=True)
            return redirect('/')

    return redirect('/')

def edititem(request,nid):

    itemsid = models.Foodmenu.objects.filter(foodid=nid).first()

    if request.method == 'GET':
        form = edititemform(instance=itemsid)
        return render(request, 'edititem.html', {"form": form,"nid": nid})

    if request.method == 'POST':
        form = edititemform(request.POST,request.FILES, instance=itemsid)
        if form.is_valid():
            form.save()
            return redirect('/')

    return redirect('/')


def removeitem(request,nid):
    form = models.Foodmenu.objects.get(foodid=nid)
    form.deleted = True
    form.save()
    return redirect('/')
