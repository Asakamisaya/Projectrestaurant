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
from restaurant_app.views import foodmenuView ,menulist ,addtomenu,edititem,removeitem
router.register(r'foodmenu', foodmenuView, basename='foodmenu')


from restaurant.settings import MEDIA_ROOT

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', menulist),
    path('menuadmin/', menulist),
    path('additem/', addtomenu),
    path('edititem/<int:nid>/', edititem),
    path('removeitem/<int:nid>/', removeitem),

    url('/', include(router.urls)),
    url(r'^Media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),

]
