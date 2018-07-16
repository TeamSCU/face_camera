## <center>树莓派</center>

### 1.上传文件
- url: /camera/upload
- post: {"camera_id":1, picture: 文件对象} (文件名注意唯一性，建议caimera_id + 时间组合)

***
## <center>安卓客户端</center>
### 1.  用户注册
- url： /user/register
- post: 
    {
        account:hch,
        password:123,
        phone_number:123456,
        name:长长长鸿
    }
- return: 状态信息success或其他异常


### 2.用户登陆
- url: /user/login
- post: {account:hch, password:123}
- return: 登陆成功的情况下返回用户资料{"id": 3, "account": "['hch']", "password": "['123']", "name": "['长长长鸿']", "phone_number": "['123456']", "time": "2018-07-15 16:27:54"}，登录则失败返回其他错误信息

### 3.用户手机上传照片（登陆后）
- url: /user/upload
- post: {picture:文件对象} (文件名注意唯一性，建议user_id + 时间组合)

### 4.用户查看人脸识别相机拍摄的照片

### 5.查看用户手机上传的照片


***
## <center>临时测试</center>
### 查看所有已上传图片
- url: user/picture/all


***
## 注：以上url前加上主机名http://118.24.100.115:8000