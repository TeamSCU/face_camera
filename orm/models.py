# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = True` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


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
    user = models.ForeignKey('TUser', models.DO_NOTHING)
    path = models.CharField(max_length=255, unique=True)
    size = models.FloatField(blank=True, null=True)
    time = models.DateTimeField()

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
    user = models.ForeignKey('TUser', models.DO_NOTHING)

    class Meta:
        managed = True
        unique_together = ('face_uid', 'user')
        db_table = 't_uid_user'


class TUser(models.Model):
    account = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=128)
    #name = models.CharField(max_length=128, blank=True, null=True)
    phone_number = models.CharField(max_length=128, blank=True, null=False, unique=True)
    time = models.DateTimeField()
    
    class Meta:
        managed = True
        db_table = 't_user'
