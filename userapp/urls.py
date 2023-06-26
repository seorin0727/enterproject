"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from . import views

urlpatterns = [
    ### http://127.0.0.1:8000/user
    path('', views.userindex, name='userpage'),
    ### http://127.0.0.1:8000/user/login
    path('login/', views.userlogin, name='loginpage'),
    ### http://127.0.0.1:8000/user/signup
    path('signup/', views.usersignup, name='signuppage'),
    ### http://127.0.0.1:8000/user/signup
    path('menu/', views.usermenu),
    ### http://127.0.0.1:8000/user/menu/capture
    path('menu/capture/', views.menucapture, name='capturepage'),
    ### http://127.0.0.1:8000/user/menu/insert
    path('menu/daily/', views.menudaily, name='dailypage'),
    ### http://127.0.0.1:8000/user/menu/insert
    path('menu/week/', views.menuweekly, name='weeklypage'),
    ### http://127.0.0.1:8000/user/search
    path('menu/search/', views.search_food, name='search_food'),
    ### http://127.0.0.1:8000/user/select_foods
    path('select_foods/', views.select_foods, name='select_foods'),
    ## http://127.0.0.1:8000/user/select_foods
    path('save_foods/', views.save_foods, name='save_foods'),
    ### http://127.0.0.1:8000/user/search
    path('menu/result/', views.showresult, name='showresult'),

]
