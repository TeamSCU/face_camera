# Generated by Django 2.0.5 on 2019-03-06 11:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('orm', '0002_auto_20190222_1137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tpicturecamera',
            name='time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]