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
from .models import Foodmenu,Foodcategory
from .serializers import FoodmenuSerializer
from restaurant_app import models
from rest_framework import viewsets, mixins

from restaurant import settings


# Create your views here.

def ordermenu(request):
    queryset = models.Foodmenu.objects.filter(deleted=False)
    grouped_data = {}
    for item in queryset:
        catename = item.catename
        if catename not in grouped_data:
            grouped_data[catename] = []
        grouped_data[catename].append(item)

    return render(request, 'Ordermenu.html', {'grouped_data': grouped_data})

#def ordermenu(request):
   # queryset = models.Foodmenu.objects.filter(deleted=False)
   # return render(request,'Ordermenu.html',{'queryset':queryset})

def menulist(request):
    queryset = models.Foodmenu.objects.filter(deleted=False)
    grouped_data = {}
    for item in queryset:
        catename = item.catename
        if catename not in grouped_data:
            grouped_data[catename] = []
        grouped_data[catename].append(item)

    return render(request, 'MenuAdmin.html', {'grouped_data': grouped_data})


#def menulist(request):
 #   queryset = models.Foodmenu.objects.filter(deleted=False)
  #  return render(request,'MenuAdmin.html',{'queryset':queryset})

def removeditems(request):
    queryset = models.Foodmenu.objects.filter(deleted=True)
    return render(request,'RecycleBin.html',{'queryset':queryset})



class addcatagoryform(forms.ModelForm):
    class Meta:
        model = Foodcategory
        fields = ['catename']

class addmenuform(forms.ModelForm):
    class Meta:
        model = Foodmenu
        fields = ['catename','foodname', 'description', 'price', 'img']

    def __init__(self, *args, **kwargs):
        super(addmenuform, self).__init__(*args, **kwargs)
        self.fields['img'].required = False
        self.fields['catename'].required = False
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control","placeholder": field.label}

class edititemform(forms.ModelForm):
    class Meta:
        model = Foodmenu
        # fields = "__all__"
        # exclude = ('foodid',)
        fields = ['catename','foodname', 'description', 'price', 'img']

    def __init__(self, *args, **kwargs):
        super(edititemform, self).__init__(*args, **kwargs)
        self.fields['catename'].required = False
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control","placeholder": field.label}



def addcatagory(request):
    if request.method == 'GET':
        addcatagory = addcatagoryform()
        return render(request, 'addcatagory.html', {"form":addcatagory})

    if request.method == 'POST':

        addcatagory = addcatagoryform(request.POST,request.FILES)
        if addcatagory.is_valid():
            addcatagory.save(commit=True)
            return redirect('/')



def addtomenu(request):

    if request.method == 'GET':
        addtomenuform = addmenuform()
        return render(request, 'addmenu.html', {"form":addtomenuform})

    if request.method == 'POST':

        addtomenuform = addmenuform(request.POST,request.FILES)
        if addtomenuform.is_valid():
            addtomenuform.save(commit=True)
            return redirect('/')

    return redirect('/')

def edititem(request,nid):

    itemsid = models.Foodmenu.objects.filter(foodid=nid).first()

    if request.method == 'GET':
        edittheitemform = edititemform(instance=itemsid)
        return render(request, 'edititem.html', {"form": edittheitemform,"nid": nid})

    if request.method == 'POST':
        edittheitemform = edititemform(request.POST,request.FILES, instance=itemsid)
        if edittheitemform.is_valid():
            edittheitemform.save()
            return redirect('/')

    return redirect('/')


def removeitem(request,nid):
    removeitem = models.Foodmenu.objects.get(foodid=nid)
    removeitem.deleted = True
    removeitem.save()
    return redirect('/')

def retrieveitem(request,nid):
    retrieveitem = models.Foodmenu.objects.get(foodid=nid)
    retrieveitem.deleted = False
    retrieveitem.save()
    return redirect('/removeditems/')

def deleteitems(request,nid):
    deleteitems = models.Foodmenu.objects.get(foodid=nid)
    deleteitems.delete()
    return redirect('/removeditems/')