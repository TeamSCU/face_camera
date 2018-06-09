# Generated by Django 2.0.5 on 2018-06-09 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orm', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tcamera',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='tpicturecamera',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='tpictureuser',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='tuidpicture',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='tuiduser',
            options={'managed': False},
        ),
        migrations.AddField(
            model_name='tuser',
            name='biography',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
        migrations.AddField(
            model_name='tuser',
            name='name',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='tuser',
            name='phone_number',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='tuser',
            name='account',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='tuser',
            name='password',
            field=models.CharField(max_length=128),
        ),
    ]