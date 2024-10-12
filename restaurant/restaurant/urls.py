"""
URL configuration for restaurant project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import re_path as url
from django.contrib import admin
from django.urls import path, include
from django.views.static import serve


from rest_framework import routers
router = routers.DefaultRouter()
from restaurant_app.views import ordermenu, menulist, addtomenu, addcatagory, edititem, removeitem, removeditems, retrieveitem ,deleteitems,submitorder,soldoutitem,removedsoldout,kitchen,cancleitem,Ocancleitem,kookingitem,finishitem,Checkout,curretorder,customercancleitem,Orders



from restaurant.settings import MEDIA_ROOT

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Order/<int:nid>/', ordermenu),
    path('Order/<int:nid>/submitorder/', submitorder),
    path('Order/<int:nid>/curretorder/', curretorder),



    path('kitchen/', kitchen),
    path('OrdersBoard/', Orders),
    path('cancleitem/<str:table_number>/<str:order_id>/<str:logid>',cancleitem),
    path('cancleitem/<str:table_number>/<str:order_id>/<str:logid>',Ocancleitem),

    path('customercancleitem/<str:table_number>/<str:order_id>/<str:logid>', customercancleitem),
    path('kookingitem/<str:table_number>/<str:order_id>/<str:logid>',kookingitem),
    path('finishitem/<str:table_number>/<str:order_id>/<str:logid>', finishitem),

    path('checkout/<str:order_id>/', Checkout),

    path('', menulist),
    path('menuadmin/', menulist),
    path('additem/', addtomenu),
    path('addcatagory/', addcatagory),
    path('edititem/<int:nid>/', edititem),
    path('removeditems/', removeditems),
    path('removeitem/<int:nid>/', removeitem),
    path('removeditems/retrieve/<int:nid>/', retrieveitem),
    path('deleteitems/<int:nid>/', deleteitems),
    path('soldoutitem/<int:nid>/', soldoutitem),
    path('removedsoldout/<int:nid>/', removedsoldout),



    url('/', include(router.urls)),
    url(r'^Media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),

]
