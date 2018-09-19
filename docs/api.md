## 树莓派

### 1.上传文件
- url: /camera/upload
- post: {"camera_id":1, picture: 文件对象} (文件名注意唯一性，建议caimera_id + 时间组合)

***
## 安卓客户端
### 1.  用户注册
- url： /client/register
- post: 
    {
        account:hch,
        password:123,
        phone_number:123456
    }
- return: 状态信息success或其他异常


### 2.用户登陆
- url: /client/login
- post: {account:hch, password:123}
- return: 登陆成功的情况下返回用户资料{"id": 3, "account": "['hch']", "password": "['123']", "phone_number": "['123456']", "time": "2018-07-15 16:27:54"}，登录则失败返回其他错误信息

### 3.用户手机上传照片（登陆后）
- url: /client/upload
- post: {picture:文件对象} (文件名注意唯一性，建议user_id + 时间组合)

### 4.用户查看人脸识别相机拍摄的照片(登陆后)
- url: /client/picture/camera
- return: [{"id": 5, "camera": 1, "path": "media/camera/1/ww2.jpeg", "size": 87.83, "time": "2018-07-29 22:14:29"}]

### 5.查看用户手机上传的照片
- url: /client/picture/user
- return: [{"id": 1, "user": 1, "path": "media/user/1/ww5.jpg", "size": 256.05, "time": "2018-07-15 22:14:42"}, {"id": 2, "user": 1, "path": "media/user/1/ww1.jpg", "size": 317.17, "time": "2018-07-15 22:14:47"}, {"id": 3, "user": 1, "path": "media/user/1/479cad37d15e3ff5dcb05939af3cbce2.jpg", "size": 197.84, "time": "2018-08-01 21:24:35"}]



### 6.忘记密码
- url: /passwd/forget
- post: {phone_number:123456,new_password:123}
- return: 电话号码匹配成功则返回:“重置密码成功”；否则返回“找不到该预留号码”

### 7.重置密码
- url: /passwd/reset
- post: {old_password:123,new_password:456}
- return: 旧密码匹配成功则返回:“修改成功”；否则返回“密码输入错误”


***
## 临时测试
### 查看所有已上传图片
- url: user/picture/all


***


***
## 注：以上url前加上主机名http://118.24.100.115:8000