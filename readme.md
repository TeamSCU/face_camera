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

## 使用数据库
```python
'''MySQL创建数据库名face，使用报错请删掉所有表重新运行如下命令'''
python manage.py makemigrations
python manage.py migrate
```
