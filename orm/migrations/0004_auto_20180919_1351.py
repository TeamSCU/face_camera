# Generated by Django 2.0.5 on 2018-09-19 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orm', '0003_auto_20180919_1347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tuser',
            name='phone_number',
            field=models.CharField(blank=True, max_length=128, unique=True),
        ),
    ]
