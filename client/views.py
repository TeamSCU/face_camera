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
        filename = str(pic.path).split('/')[-1]
        response[filename] = "<a href='http://{2}/{0}{1}'>{1}</a>".format(pic.path,filename,request.get_host())
    return RESTfulResponse(response)


@csrf_exempt
def register(request):
    user = request.POST
    if not ('account' in user and 'password' in user):
        return RESTfulResponse("缺少用户名或密码")
    try:
        TUser.objects.create(**user)
        response="success"
    except BaseException as e:
        response = str(e)
    return RESTfulResponse(response)


@csrf_exempt
def login(request):
    user = dict(request.POST)
    if not ('account' in user and 'password' in user):
        return RESTfulResponse("缺少用户名或密码")
    try:
        user_check = TUser.objects.get(account=user['account'])
        if not user_check:
           return RESTfulResponse("该用户名未注册")
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
def forget_passwd(request):
    data = request.POST #[电话号码，新密码]
    user = TUser.objects.get(phone_number = data['phone_number'])
    if user:
        user.password = data['new_password']
        user.save(force_update=True)
        return RESTfulResponse('重置密码成功')
    else:
        return RESTfulResponse('找不到该预留号码')

@csrf_exempt
def update_passwd(request):
    data = request.POST #[旧密码，新密码]
    user = TUser.objects.get(account = request.session['user'])
    if user.password == data['old_password']:
        user.password = data['new_password']
        user.save(force_update=True)
        return RESTfulResponse('修改成功')
    else:
        return RESTfulResponse('密码输入错误')


@csrf_exempt
def upload_picture(request):
    '''用户上传照片'''
    if not 'user' in request.session:
        return RESTfulResponse("请登陆")
    picture = GetRequestFile(request)
    if 'error' in picture:
        return RESTfulResponse(picture)
    user = TUser.objects.get(account = request.session['user'])
    path = os.path.join(settings.MEDIA_ROOT, 'user', str(user.id))
    if not os.path.exists(path):
        os.makedirs(path)
    filepath = os.path.join(path, picture.name)
    
    with open(filepath, 'wb+') as f:
        for chunk in picture.chunks():
            f.write(chunk)
    print("user", request.session['user'])
    picture_user = {
        'path':'media/user/' + str(user.id) + '/' + picture.name,
        'size':round(os.path.getsize(filepath)/float(1024),2),
        'user':user
    }
    try:
        obj = TPictureUser.objects.create(**picture_user)
    except:
        logger.info("文件名重复，源文件被覆盖")

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

    ## 人脸检测并注册
    for face in content:
        if face['face_probability'] < 0.90:
            continue
        search_result = search(face['face_token'])['result']['user_list'][0]
        logger.info(search_result)
        if search_result['score'] < 0.8:
            uid = add(face['face_token'])
        else:
            uid = search_result['user_id']
        TUidUser.objects.create(**{'face_uid':uid,'user':user})
    return RESTfulResponse('上传成功')

@csrf_exempt
def view_picture_user(request):
    '''查看人脸相机自动拍摄的用户照片'''
    if not 'user' in request.session:
        return RESTfulResponse('请登录')
    user = TUser.objects.get(account = request.session['user'])
    pictures = TPictureUser.objects.filter(user = user)
    pictures_dict = []
    for pic in pictures:
        pic.time = pic.time.strftime('%Y-%m-%d %H:%M:%S') 
        pictures_dict.append(model_to_dict(pic))
    print(pictures_dict)
    return RESTfulResponse(pictures_dict)

@csrf_exempt
def view_picture_camera(request):
    try:
        '''查看人脸相机自动拍摄的用户照片'''
        user = TUser.objects.get(account = request.session['user'])
    except:
        return RESTfulResponse('请登录')
    uids = TUidUser.objects.filter(user = user).values('face_uid')
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