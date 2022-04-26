"""covid_detection URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from app1.views import home,usignup,ulogin,index,ulogout,contact_us,call
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home, name='home'),
    path('usignup/',usignup, name='usignup'),
    path('ulogin/',ulogin, name='ulogin'),
    path('ulogin/index',index, name='index'),
    path('ulogout/',ulogout, name='ulogout'),
    path('',contact_us, name='contact_us'),
    path('callforhelp/',call,name='call'),

]

