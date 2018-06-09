#coding:utf-8

from PIL import Image, ImageDraw
from faceopt import FaceAPI
import ImageOpt
from matplotlib import pyplot as plt
import matplotlib.patches as patches
import random


'''全局变量'''
filePath = "src/hz.jpeg" #操作检测图片路径
op_face = FaceAPI()  #创建操作对象


'''用户列表查询'''
# content = op_face.getGroupUsers()
# print(content)
# print("\n用户列表：")
# for i in range(content['result_num']):
#     print("    ",content['result'][i]['uid'])


'''人脸检测'''
content = FaceAPI.faceDetect(op_face,filePath)
print("\n检测结果：\n",content)

'''提取图片中所有人脸矩形框保存到 ./src/face 路径下'''
result = content['result']
face_boxes = []
img = Image.open(filePath, "r") 
for i in range(0, (result['face_num'])):
    if (result['face_list'][i]['face_probability'] > 0.5): #人脸可能性大于0.7
        round_Baidu = result['face_list'][i]['location']
        round_Image = [
            #坐标调整
            round_Baidu['left'] - round_Baidu['width']/3,
            round_Baidu['top']- round_Baidu['height']/3,
            round_Baidu['left'] + round_Baidu['width']*4/3,
            round_Baidu['top'] + round_Baidu['height']*4/3
        ]
        face_boxes.append(round_Image)
        img = ImageOpt.draw(img, round_Image[0],round_Image[1],round_Image[2],round_Image[3])
img.show()#显示图片



'''将所有人脸框剪切下来并打印'''
# print("\n剪切下的人脸矩形框：\n", face_boxes)
img = Image.open(filePath, "r")

for i in range(0,len(face_boxes)):
    print("\n剪切下的人脸矩形框：\n", round,i)
    round = face_boxes[i]
    x = img.crop(box = round)
    new_File = "src/face/" + filePath[4:len(filePath)-5]+ "_new" + str(i) + ".jpg"
    x.save(new_File)


"""    
    #进行人脸查找
    content_find = op_face.identify(new_File)
    print("\n查找结果：\n",content_find)

    #查找失败注册人脸
    if(content_find == None):
        '''生成随机uid'''
        add_uid = ''.join(random.choice("abcdefg12346") for _ in range(15))

        content_add = op_face.addUser(new_File, add_uid)
        if(content_add.has_key('error_msg')):
            print("\n注册失败:", content_add['error_msg'])
        else:
            print("\n注册成功:",add_uid)
"""
