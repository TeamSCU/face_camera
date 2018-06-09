#coding:utf-8
from PIL import Image, ImageDraw



"""
绘制人脸矩形框
"""
def draw(imageObject, x0=0,y0=0,x1=0,y1=0, **swargs):
    #参数：image对象、左上角和右下角像素坐标
    draw = ImageDraw.Draw(imageObject)
    draw.rectangle((x0+1,y0+1,x1+1,y1+1),outline='red')
    draw.rectangle((x0,y0,x1,y1),outline='red')
    draw.rectangle((x0-1,y0-1,x1-1,y1-1),outline='red')
    return imageObject
