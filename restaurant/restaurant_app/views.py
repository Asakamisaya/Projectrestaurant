import os.path
import json
from collections import defaultdict
from idlelib.rpc import request_queue
from importlib.resources import files
from itertools import filterfalse
from lib2to3.fixes.fix_input import context
from tabnanny import check

from PIL.ImageOps import posterize
from django.contrib.auth.models import update_last_login
from django.core.files.storage import FileSystemStorage
from django.core.signals import request_started
from django.db.models import Max
from django.shortcuts import render, redirect
from django import forms
from django.http import HttpResponse
from rest_framework.templatetags.rest_framework import items

from .models import Foodmenu,Foodcategory,Customerorder,Receipt
from .serializers import FoodmenuSerializer
from restaurant_app import models
from rest_framework import viewsets, mixins

from restaurant import settings
from django.db.models import Sum
from datetime import timedelta
from django.utils import timezone
import calendar



# Create your views here.
def QR(request):
    return render(request, 'QR.html')

def curretorder(request,nid):
    orders = Customerorder.objects.filter(paid=False,table_number=nid)
    orderlist = {}
    for order in orders:
        foodname = Foodmenu.objects.get(foodid=order.food)
        price = Foodmenu.objects.get(foodid=order.food).price
        subtotal = int(order.quantity) * float(price)
        orderlist.setdefault(order.order_id, [])
        orderlist[order.order_id].append({
            'table_number': order.table_number,
            'foodid' : order.food,
            'foodname': foodname,
            'quantity': order.quantity,
            'price': price,
            'subtotal': subtotal,
            'Srequest':order.Srequest,
            'cancled': order.cancled,
            'cooking': order.cooking,
            'finished': order.finished,
            'logid': order.logid,
        })

    return render(request,'curretorder.html',{'orderlist': orderlist})

def Orders(request):
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
            'logid': order.logid,
        })
    #print(orderlist)

    return render(request, 'Orders.html', {'orderlist': orderlist})


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
            'Srequest': order.Srequest,
            'cancled': order.cancled,
            'cooking': order.cooking,
            'finished': order.finished,
            'logid': order.logid,
        })
    #print(orderlist)
    return render(request, 'Kitchen.html', {'orderlist': orderlist})

def customercancleitem(request,table_number,logid,order_id):
    cancleitem = models.Customerorder.objects.get(table_number=table_number,order_id=order_id,logid=logid)
    Cooking = cancleitem.cooking
    print(cancleitem)
    if Cooking == False:
        cancleitem.cancled = True
        cancleitem.delete()
        return redirect('/Order/' + table_number + '/curretorder/')
    else:
        tourl = f'/Order/{table_number}/curretorder/'
        return HttpResponse(f"""
                                <script>
                                    alert('Can not cancel,it already on kooking!');
                                    window.location.href = '{tourl}';
                                </script>
                            """)


def srequest(request,table_number,logid,order_id):
    if request.method == 'GET':
        Torder = models.Customerorder.objects.get(table_number=table_number, order_id=order_id, logid=logid)
        if Torder.Srequest:
            initial_srequest = Torder.Srequest
            Specialrequest = Srequestform(initial={'srequest': initial_srequest})
        else:
            Specialrequest = Srequestform()

        return render(request, 'Specialrequest.html', {"form":Specialrequest,'table_number':table_number,'logid':logid,'order_id':order_id})

    if request.method == 'POST':

        Specialrequest = Srequestform(request.POST)
        print(Specialrequest)
        Torder = models.Customerorder.objects.get(table_number=table_number, order_id=order_id, logid=logid)
        if Specialrequest.is_valid():
            Torder.Srequest=Specialrequest.cleaned_data['srequest']
            Torder.save()
            return redirect('/Order/' + table_number + '/curretorder/')







def Ocancleitem(request,table_number,logid,order_id):
    cancleitem = models.Customerorder.objects.get(table_number=table_number,order_id=order_id,logid=logid)
    cancleitem.cancled = True
    cancleitem.save()
    checkordsers = models.Customerorder.objects.filter(table_number=table_number, order_id=order_id, cancled=False)
    if not checkordsers:
        clean = models.Customerorder.objects.filter(table_number=table_number, order_id=order_id, cancled=True)
        for item in clean:
            item.paid = True
            item.save()
    return redirect('/OrdersBoard')

def cancleitem(request,table_number,logid,order_id):
    cancleitem = models.Customerorder.objects.get(table_number=table_number,order_id=order_id,logid=logid)
    cancleitem.cancled = True
    cancleitem.save()
    checkordsers = models.Customerorder.objects.filter(table_number=table_number,order_id=order_id,cancled= False)
    if not checkordsers:
        clean = models.Customerorder.objects.filter(table_number=table_number, order_id=order_id, cancled=True)
        for item in clean:
            item.paid=True
            item.save()
    return redirect('/kitchen')

def kookingitem(request,table_number, logid,order_id):
    kookingitem = models.Customerorder.objects.get(table_number=table_number,order_id=order_id,logid=logid)
    kookingitem.cooking = True
    kookingitem.save()
    return redirect('/kitchen')

def finishitem(request,table_number, logid,order_id):
    finishitem = models.Customerorder.objects.get(table_number=table_number,order_id=order_id,logid=logid)
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

        turl = f'/Receipt/{nextid}/'

        return HttpResponse(f"""
                        <script>
                            window.open('{turl}', '_blank');
                            alert('Successful !');
                            window.location.href = '/OrdersBoard';
                            
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



def pullReceipt(request,receipt_id):
    orderid = models.Receipt.objects.get(invoice=receipt_id).order
    items = Customerorder.objects.filter(order_id=orderid)
    checklist = {}
    total = 0
    for item in items:
        price = item.price
        subtotal = int(item.quantity) * float(price)
        subtotal = f"{subtotal:.2f}"
        total = float(total) + float(subtotal)
        total = f"{total:.2f}"
        checklist.setdefault(item.order_id, [])
        checklist[item.order_id].append({
            'InvoiceID': receipt_id,
            'orderid':orderid,
            'table_number': item.table_number,
            'foodid': item.food,
            'foodname': item.foodname,
            'quantity': item.quantity,
            'price': price,
            'subtotal': subtotal,
            'Total': total,
            'cancled': item.cancled,
        })
    #print(checklist)
    return render(request, 'Receipt.html', {'checklist': checklist})





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

    if request.method == 'GET':

        return redirect(f'/Order/{nid}')

    if request.method == 'POST':
        submitorderform = request.POST.get('data')
        order = json.loads(submitorderform)
        lastone = models.Customerorder.objects.filter(table_number=nid,paid = False)
        maxid = models.Customerorder.objects.last()
        print(maxid)
        if maxid:
            nextid = int(maxid.order_id) + 1
        else:
            nextid = 1

        if not lastone:
            for f in order:
                Customerorder.objects.create(
                    order_id=str(nextid).zfill(5),
                    table_number=nid,
                    food=f['Id'],
                    foodname=models.Foodmenu.objects.get(foodid=f['Id']).foodname,
                    price=models.Foodmenu.objects.get(foodid=f['Id']).price,
                    order_date=timezone.now(),
                    quantity=f['Count']
                )
        else:

            for f in order:
                Customerorder.objects.create(
                    order_id=str(lastone.last().order_id).zfill(5),
                    table_number=nid,
                    food=f['Id'],
                    foodname=models.Foodmenu.objects.get(foodid=f['Id']).foodname,
                    price=models.Foodmenu.objects.get(foodid=f['Id']).price,
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



class Srequestform(forms.Form):
    srequest = forms.CharField(max_length=200,label="special request")

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
        self.fields['description'].required = False
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control","placeholder": field.label}

class edititemform(forms.ModelForm):
    class Meta:
        model = Foodmenu
        fields = ['catename','foodname', 'description', 'price', 'img']

    def __init__(self, *args, **kwargs):
        super(edititemform, self).__init__(*args, **kwargs)
        self.fields['catename'].required = False
        self.fields['description'].required = False
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




def get_quarter(month):
    """根据月份返回当前季度"""
    if 1 <= month <= 3:
        return 1
    elif 4 <= month <= 6:
        return 2
    elif 7 <= month <= 9:
        return 3
    else:
        return 4


def get_top_bottom_foods(queryset, top_n=5):
    """获取销量最多和最少的 foodname"""
    # 按销量排序
    sorted_foods = queryset.values('foodname').annotate(total_quantity=Sum('quantity')).order_by('-total_quantity')

    if not sorted_foods:
        return [], []  # 如果查询结果为空，返回两个空列表

    # 获取销量最多的 TOP 5
    top_foods = sorted_foods[:top_n]

    # 获取销量最少的 BOTTOM 5（按销量升序排列）
    bottom_foods = queryset.values('foodname').annotate(total_quantity=Sum('quantity')).order_by('total_quantity')[
                   :top_n]

    return top_foods, bottom_foods

def statistics(request):
    today = timezone.now().date()
    current_year = today.year
    current_month = today.month
    current_quarter = get_quarter(current_month)

    # 年度总额
    year_total = Receipt.objects.filter(recept_date__year=current_year).aggregate(Sum('payment_amout'))[
                     'payment_amout__sum'] or 0

    # 季度总额


    if current_quarter == 1:
        quarter_start = f"{current_year}-01-01"
        quarter_end = f"{current_year}-03-31"
    elif current_quarter == 2:
        quarter_start = f"{current_year}-04-01"
        quarter_end = f"{current_year}-06-30"
    elif current_quarter == 3:
        quarter_start = f"{current_year}-07-01"
        quarter_end = f"{current_year}-09-30"
    else:
        quarter_start = f"{current_year}-10-01"
        quarter_end = f"{current_year}-12-31"

    quarter_total = Receipt.objects.filter(recept_date__range=[quarter_start, quarter_end]).aggregate(Sum('payment_amout'))[
        'payment_amout__sum'] or 0



    # 月度总额
    month_total = Receipt.objects.filter(recept_date__year=current_year, recept_date__month=current_month).aggregate(
        Sum('payment_amout'))['payment_amout__sum'] or 0


    # 当日总额
    day_total = Receipt.objects.filter(recept_date=today).aggregate(Sum('payment_amout'))['payment_amout__sum'] or 0

    # 每月销售额
    monthly_totals = []
    for month in range(1, 13):
        monthly_total = Receipt.objects.filter(recept_date__year=current_year, recept_date__month=month).aggregate(
            Sum('payment_amout'))['payment_amout__sum'] or 0
        month_name = calendar.month_abbr[month]
        monthly_totals.append({'month': month_name, 'total': monthly_total})


    def set_quarter(quarter, year):
        if quarter == 1:
            return f"{year}-01-01", f"{year}-03-31"
        elif quarter == 2:
            return f"{year}-04-01", f"{year}-06-30"
        elif quarter == 3:
            return f"{year}-07-01", f"{year}-09-30"
        elif quarter == 4:
            return f"{year}-10-01", f"{year}-12-31"
    quarterly_totals = []
    for quarter in range(1, 5):
        quarter_name = f"Q{quarter}"
        quarter_start, quarter_end = set_quarter(quarter, current_year)
        quarterly_total = Receipt.objects.filter(
            recept_date__range=[quarter_start, quarter_end]
        ).aggregate(Sum('payment_amout'))['payment_amout__sum'] or 0
        quarterly_totals.append({'quarter': quarter_name, 'total': quarterly_total})
        # 近三年每年数据


    yearly_totals = []
    for year in range(current_year, current_year-3,-1):
        yearly_total = Receipt.objects.filter(recept_date__year=year).aggregate(
           Sum('payment_amout'))['payment_amout__sum'] or 0
        yearly_totals.append({'year': year, 'total': yearly_total})

        # 近一周每天数据
    daily_totals = []
    for day in range(7):
        date = today - timedelta(days=day)
        daily_total = Receipt.objects.filter(recept_date=date).aggregate(
            Sum('payment_amout'))['payment_amout__sum'] or 0
        weekdate = calendar.day_abbr[date.weekday()]
        daily_totals.append({'date': weekdate, 'total': daily_total})

        # 今年总订单数
    year_totalcount = Customerorder.objects.filter(cancled =False,paid=True, order_date__year=current_year).count()

    # 本月总订单数
    month_totalcount = Customerorder.objects.filter(cancled =False,paid=True, order_date__year=current_year,order_date__month=current_month).count()

    # 本日总订单数
    day_totalcount = Customerorder.objects.filter(cancled =False,paid=True, order_date=today).count()

    paid_orders = Customerorder.objects.filter(paid=True, cancled=False)

    # 当年数据筛选
    yearly_orders = paid_orders.filter(order_date__year=current_year)

    # 当月数据筛选
    monthly_orders = paid_orders.filter(order_date__year=current_year, order_date__month=current_month)

    # 获取当年 TOP 5 和 Bottom 5
    top_yearly_foods, bottom_yearly_foods = get_top_bottom_foods(yearly_orders)

    # 获取当月 TOP 5 和 Bottom 5
    top_monthly_foods, bottom_monthly_foods = get_top_bottom_foods(monthly_orders)

    # 将结果传递给模板
    context = {
        'year_total': year_total,
        'quarter_total': quarter_total,
        'month_total': month_total,
        'day_total': day_total,
        'year_totalcount': year_totalcount,
        'month_totalcount': month_totalcount,
        'day_totalcount': day_totalcount,
        'monthly_totals': monthly_totals,
        'quarterly_totals': quarterly_totals,
        'yearly_totals': yearly_totals,
        'daily_totals': daily_totals,
        'top_yearly_foods': top_yearly_foods,
        'bottom_yearly_foods': bottom_yearly_foods,
        'top_monthly_foods': top_monthly_foods,
        'bottom_monthly_foods': bottom_monthly_foods,
    }
    print(context)
    return render(request, 'statistics.html', context)


