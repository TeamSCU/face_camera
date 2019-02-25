from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register([TCamera, TPictureUser])

@admin.register(TPictureCamera)
class TPictureCameraAdmin(admin.ModelAdmin):
    list_display = ('id', 'path', 'size')
    fk_fields = ('user')