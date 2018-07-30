## 先fork
## 环境要求
>建议使用python或conda虚拟环境
+ python3.6  
+ pip install Django==2.0.5  
+ pip install baidu-aip  

## 模块说明
+ face_camera\
  项目根模块
+ client\
  手机客户端
+ orm\
  数据库
+ baidu_api\
  api操作

## 交互接口
数据交互接口文档请浏览docs/api.md

## detail
相机照片发送到后端，存到t_picture_camera.调用人脸检测，返回face_token的列表，
使用该face_token列表进行1:N人脸搜索，如果匹配到已存
在的人脸照片，则将uid和picture加入到t_uid_picture