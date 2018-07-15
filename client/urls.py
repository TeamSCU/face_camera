from django.urls import path
from . import views

urlpatterns = [
    path('picture/all', views.listAll),
    path('register', views.register),
    path('login', views.login),
    path('upload', views.upload_picture),
]
