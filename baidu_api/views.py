from django.shortcuts import render, redirect
from django.http import HttpResponse
import json, face_camera, sys, os
from django.conf import settings
from django.db import models
from django.views.decorators.csrf import csrf_exempt
from orm.models import *
from baiduHttp import *
import logging, uuid

logger = logging.getLogger('django')

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
    ## 保存图片到本地和数据库
    path = os.path.join(settings.MEDIA_ROOT, 'camera', camera_id)
    if not os.path.exists(path):
        os.makedirs(path)
    filepath = os.path.join(path, picture.name)

    with open(filepath, 'wb+') as f:
        for chunk in picture.chunks():
            f.write(chunk)
    picture_obj = {
        "camera":TCamera.objects.get(id=camera_id),
        "size": round(os.path.getsize(filepath)/float(1024),2),
        "path":"media/camera/"+ camera_id + '/' + picture.name
    }
    response = "success"

    ## 文件名相同将会覆盖
    try:
        obj = TPictureCamera.objects.create(**picture_obj)# 创建图片数据库对象
    except:
        obj = TPictureCamera.objects.get(path = picture_obj['path'])
        logger.info('覆盖文件：'+ filepath)

    logger.info(obj.id)
    ## 人脸检测
    try:
        content = detect(filepath)['result']['face_list']
        logger.debug(content)
    except BaseException as e:
        ## 照片中没有人脸,删除数据库和照片文件
        logger.debug(str(e))
        os.remove(filepath)
        obj.delete()
        return RESTfulResponse('没有检测到人脸')

    # 树莓派照片人脸检测并注册
    for face in content:
        if face['face_probability'] < 0.90:
            continue
        search_result = search(face['face_token'])['result']['user_list'][0]
        logger.info(search_result)
        if search_result['score'] < 70:
            uid = add(face['face_token'])
        else:
            uid = search_result['user_id']
        TUidPicture.objects.create(**{'uid':uid,'picture':obj})

    return RESTfulResponse(response)
