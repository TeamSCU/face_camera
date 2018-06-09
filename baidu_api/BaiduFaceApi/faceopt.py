# coding=utf-8
'''
百度API操作模块:
人脸库管理
获取token
人脸检测
人脸识别
人脸查找
'''
import urllib3, urllib, sys
from aip import AipFace
import ssl
import base64

#全局变量
groupId = "test" #测试期间使用此人脸组


class FaceAPI:
    #人脸检测、识别、查找
    APP_ID="10924555"
    API_KEY = 'bSLIy2ualt16mEUMxNcFL9FX'
    SECRET_KEY = 'Tq2PrrEQqNavQrm12DBdfcqOaZHxikSW'
    client = AipFace(APP_ID,API_KEY,SECRET_KEY)
    imageType = "BASE64"

    def __get_file_content(self, filePath):
        with open(filePath, 'rb') as fp:
            return base64.b64encode(fp.read())


    def faceDetect(self, filePath):
        #调用人脸检测API,返回完整content
        image = self.__get_file_content(filePath)
        options = {"max_face_num":10} #请求参数
        getValue = self.client.detect(image, self.imageType, options)
        return getValue

    def identify(self,filePath):
        #一对多人脸查找
        image = self.__get_file_content(filePath)
        """ 如果有可选参数 """
        options = {"user_top_num":1}
        """ 带参数调用人脸识别 """
        getValue = self.client.identifyUser(groupId, image, options)
        '''查找错误'''
        if (getValue.has_key("error_msg")):
            print("faceopt ->",getValue['error_msg'])
            return
        '''未找到匹配较高的用户'''
        if (max(getValue['result'][0]['scores']) < 70):
            return
        return getValue


    def multiIdentify(self, filePath):
        #多对多查找
        image = self.__get_file_content(filePath)
        """ 调用M:N 识别 (无参数)"""
        # self.client.multiIdentify(groupId, image)
        """ 如果有可选参数 """
        options = {"user_top_num": 1, "detect_top_num":10}
        """ 带参数调用M:N 识别 """
        getValue = self.client.multiIdentify(groupId, image, options)
        return getValue 


    def addUser(self,filePath, uid, userInfo="user's default info"):
        #人脸注册
        image = self.__get_file_content(filePath)

        """ 调用无参数人脸注册 """
        # self.client.addUser(uid, userInfo, groupId, image)

        """ 如果有可选参数 """
        options = {"action_type" : "append"}

        """ 带参数调用人脸注册 """
        getValue = self.client.addUser(uid, userInfo, groupId, image, options)
        return getValue


    def getGroupUsers(self):
        """ 调用组内用户列表查询 """
        self.client.getGroupUsers(groupId)

        """ 如果有可选参数 """
        options = {"start":0, "num":50}

        """ 带参数调用组内用户列表查询 """
        getValue = self.client.getGroupUsers(groupId, options)
        return getValue

    def deleteUser(self, uid):
        """ 调用组内删除用户 """
        getValue = self.client.deleteGroupUser(groupId, uid)
        if(getValue.has_key("error_msg")):
            print("faceopt -> 删除失败", getValue['msg'])
        else:
            print("faceopt -> 删除成功！")
