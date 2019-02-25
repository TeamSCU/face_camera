from django.shortcuts import render, redirect
from django.http import HttpResponse
import json, face_camera, sys, os
from django.conf import settings
from django.db import models
from django.views.decorators.csrf import csrf_exempt
from orm.models import *
from django.forms.models import model_to_dict
import logging
from baiduHttp import *

logger = logging.getLogger('django')

def RESTfulResponse(data):
    return HttpResponse(json.dumps(data, ensure_ascii=False))

status = ['SUCCESS','LOGIN_ERROR','NO_FACE','DUPLI_FILE_NAME']

#解析请求数据
#解析上传文件
def GetRequestFile(request):
    response = {}
    if request.method == 'POST':
        try:
            file_name = list(request.FILES.keys())[0]
            picture = request.FILES.get(file_name)
            picture.name = file_name+'.jpg'
            return picture
        except BaseException as e:
            print(str(e))
            response = {'error': str(e)}
    else:
        response = {'error': "请使用post方法"}
    return response


def listAll(request):
    '''返回数据库中所有人脸相机图片url'''
    response = {}
    pictures = TPictureCamera.objects.all()
    for pic in pictures:
        filename = str(pic.path).split('/')[-1]
        response[filename] = "<a href='http://{2}/{0}{1}'>{1}</a>".format(pic.path,filename,request.get_host())
    return RESTfulResponse(response)


@csrf_exempt
def upload_picture(request):
    '''用户上传照片'''

    # 解析请求用户图片
    picture = GetRequestFile(request)
    filename = picture.name
    
    # 空文件对象
    if not picture:
        return RESTfulResponse('上传图片为空') 
    
    if 'error' in picture:
        return RESTfulResponse(picture)
    account = request.POST['account']

    # 保存图片
    path = os.path.join(settings.MEDIA_ROOT, 'user', account)
    if not os.path.exists(path):
        os.makedirs(path)
    filepath = os.path.join(path, filename)
    with open(filepath, 'wb+') as f:
        for chunk in picture.chunks():
            f.write(chunk)

    picture_user = {
        'path':'media/user/' + account + '/' + filename,
        'size':round(os.path.getsize(filepath)/float(1024),2),
        'account':account
    }
    try:
        obj = TPictureUser.objects.create(**picture_user)
    except:
        logger.info("文件名重复，源文件被覆盖")
        obj = TPictureUser.objects.get(path=picture_user['path'])

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

    ## 人脸检测并注册,建立百度uid与user索引项
    for face in content:
        if face['face_probability'] < 0.90:
            continue
        search_result = search(face['face_token'])['result']
        logger.info(search_result)

        if search_result:
            try:
                search_result = search_result['user_list'][0]
            except:
                pass

        if (not search_result) or search_result['score'] < 0.8:
            uid = add(face['face_token'])
        else:
            uid = search_result['user_id']
        try:
            TUidUser.objects.create(**{'face_uid': uid, 'account': account})
        except Exception as e:
            logger.info(str(e))
    return RESTfulResponse('上传成功')

@csrf_exempt
def view_picture_user(request):
    '''查看用户自己上传的照片'''

    account = request.POST['account']
    pictures = TPictureUser.objects.filter(account = account)

    pictures_dict = []
    for pic in pictures:
        pic.time = pic.time.strftime('%Y-%m-%d %H:%M:%S') 
        pictures_dict.append(model_to_dict(pic))
    print(pictures_dict)
    return RESTfulResponse(pictures_dict)

@csrf_exempt
def delete_picture_camera(request):
    """删除用户选择的树莓派照片"""
    to_delete_ids = request.POST['delete_ids']
    for id in to_delete_ids:
        try:
            pic = TPictureCamera.objects.get(id=id)
            path = pic.path
            os.remove(path)
            pic.delete()
        except Exception as e:
            print(str(e))
    return RESTfulResponse('删除完成')


@csrf_exempt
def view_picture_camera(request):
    '''查看人脸相机自动拍摄的用户照片'''
    account = request.POST['account']
    uids = TUidUser.objects.filter(account = account).values('face_uid')
    pictures = []

    for uid in uids:
        picture_cur = TUidPicture.objects.filter(uid = uid['face_uid']).values('picture_id')
        pictures += [p['picture_id'] for p in picture_cur]
    pictures = set(pictures)
    paths = []
    for pic_id in pictures:
        pic_obj = TPictureCamera.objects.get(id=pic_id)
        pic_obj.time = pic_obj.time.strftime('%Y-%m-%d %H:%M:%S')
        paths.append(model_to_dict(pic_obj))
    return RESTfulResponse(paths)