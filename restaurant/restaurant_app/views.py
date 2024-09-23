import os.path
import json
from collections import defaultdict
from idlelib.rpc import request_queue
from importlib.resources import files
from itertools import filterfalse
from lib2to3.fixes.fix_input import context

from PIL.ImageOps import posterize
from django.contrib.auth.models import update_last_login
from django.core.files.storage import FileSystemStorage
from django.core.signals import request_started
from django.db.models import Max
from django.shortcuts import render, redirect
from django import forms
from django.http import HttpResponse
from .models import Foodmenu,Foodcategory,Customerorder,Receipt
from .serializers import FoodmenuSerializer
from restaurant_app import models
from rest_framework import viewsets, mixins

from restaurant import settings
from django.utils import timezone


# Create your views here.



def kitchen(request):
    orders = Customerorder.objects.filter(paid=False)
    orderlist = {}
    for order in orders:
        foodname = Foodmenu.objects.get(foodid=order.food)
        orderlist.setdefault(order.order_id, [])
        orderlist[order.order_id].append({
            'table_number': order.table_number,
            'foodid' : order.food,
            'foodname': foodname,
            'quantity': order.quantity,
            'cancled': order.cancled,
            'cooking': order.cooking,
            'finished': order.finished,
        })
    #print(orderlist)

    return render(request, 'Kitchen.html', {'orderlist': orderlist})

def cancleitem(request,table_number, foodid,order_id):
    cancleitem = models.Customerorder.objects.get(table_number=table_number,order_id=order_id,food=foodid, )
    cancleitem.cancled = True
    cancleitem.save()
    return redirect('/kitchen')

def kookingitem(request,table_number, foodid,order_id):
    kookingitem = models.Customerorder.objects.get(table_number=table_number,order_id=order_id,food=foodid, )
    kookingitem.cooking = True
    kookingitem.save()
    return redirect('/kitchen')

def finishitem(request,table_number, foodid,order_id):
    finishitem = models.Customerorder.objects.get(table_number=table_number,order_id=order_id,food=foodid, )
    finishitem.finished = True
    finishitem.save()
    return redirect('/kitchen')






def Checkout(request,order_id):
    maxid = Receipt.objects.order_by('invoice').last()
    print(maxid)
    if maxid:
        nextid = str(int(maxid.invoice)+1).zfill(6)
    else:
        nextid = str(1).zfill(6)
    if request.method == 'POST':
        method = request.POST.get('option')
        orders = Customerorder.objects.filter(order_id=order_id)
        total = 0
        for items in orders:
            if items.cancled == False:
                p = Foodmenu.objects.get(foodid=items.food).price
                total = total + int(items.quantity) * float(p)
            items.paid = True
            items.save()

        Receipt.objects.create(
            invoice=str(nextid).zfill(5),
            order=order_id,
            payment_method=method,
            recept_date=timezone.now(),
            payment_amout=total
        )

        return HttpResponse("""
                        <script>
                            alert('Successful !');
                            window.location.href = '/kitchen';
                        </script>
                    """)

    if Customerorder.objects.filter(order_id=order_id, cancled=False):
        orderlist = Customerorder.objects.filter(order_id=order_id)
        checklist = {}
        for order in orderlist:
            foodname = Foodmenu.objects.get(foodid=order.food)
            price =  Foodmenu.objects.get(foodid=order.food).price
            subtotal =  int(order.quantity) * float(price)
            subtotal = f"{subtotal:.2f}"
            checklist.setdefault(order.order_id, [])
            checklist[order.order_id].append({
                'InvoiceID':nextid,
                'table_number': order.table_number,
                'foodid' : order.food,
                'foodname': foodname,
                'quantity': order.quantity,
                'price' : price,
                'subtotal': subtotal,
                'cancled': order.cancled,
                'cooking': order.cooking,
                'finished': order.finished,
            })
        #print(checklist)

        return render(request,'Checkout.html',{'checklist': checklist})

    else:
        orders = Customerorder.objects.filter(order_id=order_id)
        for items in orders:
            items.paid = True
            items.save()
        return HttpResponse("""
                        <script>
                            alert('There are no items to checkout, the order will be deleted !');
                            window.location.href = '/kitchen';
                        </script>
                    """)



def ordermenu(request,nid):
    queryset = models.Foodmenu.objects.filter(deleted=False)
    grouped_data = {}
    for item in queryset:
        catename = item.catename
        if catename not in grouped_data:
            grouped_data[catename] = []
        grouped_data[catename].append(item)

    return render(request, 'Ordermenu.html', {'grouped_data': grouped_data})


def submitorder(request,nid):

    if request.method == 'POST':

        submitorderform = request.POST.get('data')
        order = json.loads(submitorderform)
        lastone = models.Customerorder.objects.filter(table_number=nid,paid = False)
        maxid = Customerorder.objects.order_by('order_id').last()

        if lastone:
            if maxid:
                nextid = int(maxid.order_id) + 1
            else:
                nextid = 1
            for f in order:
                Customerorder.objects.create(
                    order_id=str(nextid).zfill(5),
                    table_number=nid,
                    food=f['Id'],
                    order_date=timezone.now(),
                    quantity=f['Count']
                )
        else:
            nextid = int(maxid.order_id)
            for f in order:
                Customerorder.objects.create(
                    order_id=str(nextid).zfill(5),
                    table_number=nid,
                    food=f['Id'],
                    order_date=timezone.now(),
                    quantity=f['Count']
                )


    return redirect(f'/Order/{nid}')


def menulist(request):
    queryset = models.Foodmenu.objects.filter(deleted=False)
    grouped_data = {}
    for item in queryset:
        catename = item.catename
        if catename not in grouped_data:
            grouped_data[catename] = []
        grouped_data[catename].append(item)

    return render(request, 'MenuAdmin.html', {'grouped_data': grouped_data})



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



def soldoutitem(request,nid):
    removeitem = models.Foodmenu.objects.get(foodid=nid)
    removeitem.soldout = True
    removeitem.save()
    return redirect('/')

def removedsoldout(request,nid):
    removeitem = models.Foodmenu.objects.get(foodid=nid)
    removeitem.soldout = False
    removeitem.save()
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
    image_path = os.path.join(settings.MEDIA_ROOT, deleteitems.img.path)
    if os.path.exists(image_path):
        os.remove(image_path)

    deleteitems.delete()
    return redirect('/removeditems/')





