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
from django.contrib.auth.views import LogoutView

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
    path('delete_user/', views.delete_user, name='delete_user'),
    path('change_password/', views.change_password, name='change_password'),
    path('send_drone_command/', views.send_drone_command, name='send_drone_command'),
    path('stream-proxy/', views.proxy_stream, name='stream-proxy'),
    path('send_command/<str:command>/', views.send_command, name='send_command'),
    path('backup/', views.trigger_backup, name='trigger_backup'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('list_users/', views.list_users, name='list_users'),
]
