# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-04-11 12:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EasyAdmin', '0018_auto_20180411_2018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='caption',
            field=models.CharField(blank=True, default='', max_length=32, verbose_name='标题'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='order',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='顺序'),
        ),
    ]
