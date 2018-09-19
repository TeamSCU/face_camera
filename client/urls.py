from django.urls import path
from . import views

urlpatterns = [
    path('picture/all', views.listAll),
    path('register', views.register),
    path('login', views.login),
    path('upload', views.upload_picture),
    path('picture/user', views.view_picture_user),
    path('picture/camera', views.view_picture_camera),
    path('./passwd/forget', views.forget_passwd),
    path('./passwd/reset', views.update_passwd),
]
