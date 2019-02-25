# encoding:utf-8
from urllib import request, parse
import json
import base64
from matplotlib import pyplot as plt
import matplotlib.patches as patches
import random

API_KEY = 'bSLIy2ualt16mEUMxNcFL9FX'
imageType = "BASE64"
headers={'Content-Type':'application/json'}

def token():
    url = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=bSLIy2ualt16mEUMxNcFL9FX&client_secret=Tq2PrrEQqNavQrm12DBdfcqOaZHxikSW&'
    response = request.urlopen(url = url)
    content = json.loads(response.read().decode())
    return content['access_token']

def post_req(url, params):
    data = parse.urlencode(params).encode('utf-8')
    url = url + "?access_token=" + token()
    req = request.Request(url, data=data, headers=headers)
    response = request.urlopen(req)
    content = json.loads(response.read().decode())
    return content

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return base64.b64encode(fp.read())
        
def detect(filepath):
    '''人脸检测与属性分析'''
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"
    params = {
        'image':get_file_content(filepath),
        'image_type':imageType,
        'max_face_num':10
    }
    return post_req(request_url,params)

def search(image,type):
    url = 'https://aip.baidubce.com/rest/2.0/face/v3/search'
    params ={
        'image':image,
        'image_type':type,
        'group_id_list':'test',
        

    }


if __name__ == '__main__':
    print(detect('./src/hz.jpeg'))