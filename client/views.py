from django.shortcuts import render, redirect
from django.http import HttpResponse
import json, face_camera, sys, os
from django.conf import settings
from django.db import models
from django.views.decorators.csrf import csrf_exempt
from orm.models import *
from django.forms.models import model_to_dict
import datetime
# Create your views here.


def RESTfulResponse(data):
    return HttpResponse(json.dumps(data, ensure_ascii=False))

#解析请求数据
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

def listAll(request):
    '''返回数据库中所有人脸相机图片url'''
    response = {}
    pictures = TPictureCamera.objects.all()
    for pic in pictures:
        response[pic.file_name] = "<a href='http://{2}/{0}{1}'>{1}</a>".format(pic.path,pic.file_name,request.get_host())
    return RESTfulResponse(response)


@csrf_exempt
def register(request):
    user = request.POST
    print(user)
    if not ('account' in user and 'password' in user):
        return RESTfulResponse("请求内容错误")
    try:
        TUser.objects.create(**user)
        response="success"
    except BaseException as e:
        response = str(e)
    return RESTfulResponse(response)

@csrf_exempt
def login(request):
    user= dict(request.POST)
    if not ('account' in user and 'password' in user):
        return RESTfulResponse("请求内容错误")
    try:
        user_check = TUser.objects.get(account = user['account'])

        if not user_check:
           return RESTfulResponse("用户账户不存在")
        else:
            # print(type(user_check.password), str(user['password']))
            if user_check.password == str(user['password']):
                user_check.time = user_check.time.strftime('%Y-%m-%d %H:%M:%S') 
                request.session['user'] = user['account'] #登陆成功
                response = model_to_dict(user_check)
            else:
                return RESTfulResponse("密码错误")
    except BaseException as e:
        response = e.__str__()
    return RESTfulResponse(response)

@csrf_exempt
def upload_picture(request):
    '''用户上船照片'''
    if not request.session['user']:
        return RESTfulResponse("请登陆")
    picture = GetRequestFile(request)
    if 'error' in picture:
        return RESTfulResponse(picture)
    filepath = os.path.join(settings.MEDIA_ROOT, 'user', picture.name)
    
    with open(filepath, 'wb+') as f:
        for chunk in picture.chunks():
            f.write(chunk)
    print("user", request.session['user'])
    picture_user = {
        'path':'media/user/' + picture.name,
        'size':round(os.path.getsize(filepath)/float(1024),2),
        'user':TUser.objects.get(account = request.session['user'])
    }
    TPictureUser.objects.create(**picture_user)
    return RESTfulResponse("success")

    @csrf_exempt
    def view_picture_camera(request):
        '''查看自动拍摄的用户照片'''