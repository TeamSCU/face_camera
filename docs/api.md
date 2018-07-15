## <center>树莓派</center>

### 1.上传文件
- url: /camera/upload
- post: {"camera_id":1, picture: 文件对象}

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

### 2.用户登陆
- url: /user/login
- post: {account:hch, password:123}

### 3.用户手机上传照片（登陆后）
- url: /user/upload
- post: {picture:文件对象}

### 4.用户查看人脸识别相机拍摄的照片

### 5.查看用户手机上传的照片



***
## <center>临时测试</center>
### 查看所有已上传图片
- url:\
/user/picture/all


***
## 注：以上url前加上主机名http://118.24.100.115:8000