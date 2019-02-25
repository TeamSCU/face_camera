# encoding:utf-8
from urllib import request, parse
import json,uuid
import base64
# from matplotlib import pyplot as plt
# import matplotlib.patches as patches
# import random

API_KEY = 'bSLIy2ualt16mEUMxNcFL9FX'
types = ['BASE64', 'URL', 'FACE_TOKEN']
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
        'image_type':types[0],
        'max_face_num':10
    }
    return post_req(request_url,params)

def search(image,type = 2):
    url = 'https://aip.baidubce.com/rest/2.0/face/v3/search'
    params ={
        'image':image,
        'image_type':types[type],
        'group_id_list': 'test'
    }
    return post_req(url, params)

def add(image, type = 2):
    url = 'https://aip.baidubce.com/rest/2.0/face/v3/faceset/user/add'
    uid = str(uuid.uuid1())
    while '-' in uid:
        uid = uid.replace('-', '')
    params = {
        'image': image,
        'image_type': types[type],
        'group_id': 'test',
        'user_id': uid
    }
    content = post_req(url, params)
    print(content)
    return uid


# def test():
#     '''提取图片中所有人脸矩形框保存到 ./src/face 路径下'''
#     filepath='src/hz.jpeg'
#     result = detect(filepath)['result']
#     face_boxes = []
#     img = Image.open(filepath, "r")
#     for i in range(0, (result['face_num'])):
#         if (result['face_list'][i]['face_probability'] > 0.5): #人脸可能性大于0.7
#             round_Baidu = result['face_list'][i]['location']
#             round_Image = [
#                 #坐标调整
#                 round_Baidu['left'] - round_Baidu['width']/3,
#                 round_Baidu['top']- round_Baidu['height']/3,
#                 round_Baidu['left'] + round_Baidu['width']*4/3,
#                 round_Baidu['top'] + round_Baidu['height']*4/3
#             ]
#             face_boxes.append(round_Image)
#             img = ImageOpt.draw(img, round_Image[0],round_Image[1],round_Image[2],round_Image[3])
#     img.show()#显示图片

#

if __name__ == '__main__':
    print(detect('./src/hz.jpeg'))