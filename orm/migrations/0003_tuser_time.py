# Generated by Django 2.0.5 on 2018-06-09 17:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('orm', '0002_auto_20180610_0152'),
    ]

    operations = [
        migrations.AddField(
            model_name='tuser',
            name='time',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
