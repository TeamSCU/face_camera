from django.urls import path
from . import views

urlpatterns = [
    path('picture/all', views.listAll),
    path('upload', views.upload_picture),
    path('picture/user', views.view_picture_user),
    path('picture/camera', views.view_picture_camera),
    path('picture/delete', views.delete_picture_camera),
]
