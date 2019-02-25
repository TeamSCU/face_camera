## 树莓派

### 1.上传文件
- url: /camera/upload
- post: {"camera_id":1, picture: 文件对象} (文件名注意唯一性，建议caimera_id + 时间组合)

***
## 安卓客户端

### 用户手机上传照片（登陆后）
- url: /client/upload
- post: {account:hch, [文件名]:文件对象} (文件名注意唯一性，建议user_id + 时间组合)

### 用户查看人脸识别相机拍摄的照片(登陆后)
- url: /client/picture/camera
- post:{account:hch}
- return: [{"id": 5, "camera": 1, "path": "media/camera/1/ww2.jpeg", "size": 87.83, "time": "2018-07-29 22:14:29"}]

### 查看用户手机上传的照片
- url: /client/picture/user
- return: [{"id": 1, "user": 1, "path": "media/user/1/ww5.jpg", "size": 256.05, "time": "2018-07-15 22:14:42"}, {"id": 2, "user": 1, "path": "media/user/1/ww1.jpg", "size": 317.17, "time": "2018-07-15 22:14:47"}, {"id": 3, "user": 1, "path": "media/user/1/479cad37d15e3ff5dcb05939af3cbce2.jpg", "size": 197.84, "time": "2018-08-01 21:24:35"}]

### 删除选择的树莓派照片
- url: /client/picture/delete
- post: {delete_ids:[1, 5, 9, 4]}
- return: 删除结果状态


***
## 临时测试
### 查看所有已上传图片
- url: user/picture/all


***


***
## 注：以上url前加上主机名http://118.24.100.115:8000