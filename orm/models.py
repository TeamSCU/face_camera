# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = True` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.utils import timezone


class TCamera(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=256, blank=True, null=True)
    address = models.CharField(max_length=256)

    class Meta:
        managed = True
        db_table = 't_camera'


class TPictureCamera(models.Model):
    camera = models.ForeignKey(TCamera, models.DO_NOTHING)
    path = models.CharField(max_length=255, unique=True)
    size = models.FloatField(blank=True, null=True)
    time = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 't_picture_camera'


class TPictureUser(models.Model):
    account = models.CharField(max_length=255, db_index=True)
    path = models.CharField(max_length=255, unique=True)
    size = models.FloatField('文件大小', blank=True, null=True)
    time = models.DateTimeField('上传时间', default = timezone.now)

    class Meta:
        managed = True
        db_table = 't_picture_user'


class TUidPicture(models.Model):
    uid = models.CharField(max_length=128)
    picture = models.ForeignKey(TPictureCamera, models.DO_NOTHING)

    class Meta:
        managed = True
        unique_together = ('uid', 'picture',)
        db_table = 't_uid_picture'


class TUidUser(models.Model):
    face_uid = models.CharField(max_length=128)
    account = models.CharField(max_length=255, db_index=True)

    class Meta:
        managed = True
        unique_together = ('face_uid', 'account')
        db_table = 't_uid_user'
