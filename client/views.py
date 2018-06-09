from django.shortcuts import render, redirect
from django.http import HttpResponse
import json, face_camera, sys, os
from django.conf import settings
from django.db import models
from django.views.decorators.csrf import csrf_exempt
from orm.models import TPictureCamera,TCamera
# Create your views here.


def RESTfulResponse(data):
    return HttpResponse(json.dumps(data, ensure_ascii=False))

#返回数据库中所有人脸相机图片url
def listAll(request):
    response = {}
    pictures = TPictureCamera.objects.all()
    for pic in pictures:
        response[pic.file_name] = "<a href='http://{2}/{0}{1}'>{1}</a>".format(pic.path,pic.file_name,request.get_host())
    return RESTfulResponse(response)