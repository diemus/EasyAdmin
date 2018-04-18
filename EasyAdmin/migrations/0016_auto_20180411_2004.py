# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-04-11 12:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EasyAdmin', '0015_auto_20180411_2003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='icon_class',
            field=models.CharField(blank=True, default='', max_length=32, verbose_name='图标类'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='url_names',
            field=models.CharField(blank=True, default='', max_length=64, verbose_name='URL Name'),
        ),
    ]
