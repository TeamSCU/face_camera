from django.shortcuts import render, redirect
from django.http import HttpResponse
import json, face_camera, sys, os
from django.conf import settings
from django.db import models
from django.views.decorators.csrf import csrf_exempt
from orm.models import TPictureCamera,TCamera
# Create your views here.

#返回请求
def RESTfulResponse(data):
    return HttpResponse(json.dumps(data, ensure_ascii=False))

#解析请求数据
def GetRequestData(request):
    response = {}
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode())
            print(data)
            return data
        except:
            print("response解析错误")
            response = {'error': "response解析错误"}
    else:
        response = {'error': "请使用post方法"}
    return response

#解析上传文件
def GetRequestFile(request):
    response = {}
    if request.method == 'POST':
        try:
            data = request.FILES.get("picture")
            return data
        except BaseException as e:
            print(str(e))
            response = {'error': "response解析错误"}
    else:
        response = {'error': "请使用post方法"}
    return response

#上传文件{"camera_id":1, picture: 文件对象}
@csrf_exempt
def upload(request):
    '''上传测试图片'''
    camera_id=(request.POST)['camera_id']
    picture = GetRequestFile(request)
    if 'error' in picture:
        return RESTfulResponse(picture)
    filepath = os.path.join(settings.MEDIA_ROOT, 'camera', picture.name)
    
    with open(filepath, 'wb+') as f:
        for chunk in picture.chunks():
            f.write(chunk)
    #创建图片数据库对象
    picture_obj = {
        "camera":TCamera.objects.get(id=camera_id),
        "size": round(os.path.getsize(filepath)/float(1024),2),
        "path":"media/camera/"+picture.name
    }
    response = "success"
    try:
        TPictureCamera.objects.create(**picture_obj)
    except BaseException as e:
        response = str(e)
    return RESTfulResponse(response)
