"""
URL configuration for DroneSecurity project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
# drone_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('stream/', views.stream, name='stream'),
    path('admin_data/', views.admin_data, name='admin_data'),
    path('problems/', views.problems_detected, name='problems_detected'),
    path('img_view/', views.img_view, name='img_view'),
    path('login/', views.login_view, name='login_view'),
    path('video_feed/', views.video_feed, name='video_feed'),
    path('about_us/', views.about_us, name='about_us'),
    path('setting/', views.setting, name='setting'),
    path('inscription/', views.inscription_view, name='inscription_view'),
]