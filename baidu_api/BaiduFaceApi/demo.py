import urllib, sys
from aip import AipFace
import ssl
import base64
import json

# #全局变量
# groupId = "test" #测试期间使用此人脸组


# class FaceAPI:
#     #人脸检测、识别、查找

#     client = AipFace(APP_ID,API_KEY,SECRET_KEY)

#     def __get_file_content(self, filePath):
#         with open(filePath, 'rb') as fp:
#             return base64.b64encode(fp.read())


#     def faceDetect(self, filePath):
#         #调用人脸检测API,返回完整content
#         image = self.__get_file_content(filePath)
#         options = {"max_face_num":10} #请求参数
#         getValue = self.client.detect(image, self.imageType, options)
#         return getValue


# test = FaceAPI()
# content = test.faceDetect('src/hz.jpeg')
# print(content)


#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys
import requests, base64, json, urllib
from aip import AipFace

APP_ID="10924555"
API_KEY = 'bSLIy2ualt16mEUMxNcFL9FX'
SECRET_KEY = 'Tq2PrrEQqNavQrm12DBdfcqOaZHxikSW'
imageType = "BASE64"

client = AipFace(APP_ID, API_KEY, SECRET_KEY)
""" 读取图片 """
f = open('src/hz.jpeg', 'rb')
# 参数images：图像base64编码
image = base64.b64encode(f.read())
imageType = "BASE64"

""" 调用人脸检测 """
client.detect(image, imageType)

""" 如果有可选参数 """
options = {}
options["face_field"] = "age"
options["max_face_num"] = 2
options["face_type"] = "LIVE"

""" 带参数调用人脸检测 """
result = client.detect(image, imageType, options)
print(json.dumps(result, ensure_ascii=False))
