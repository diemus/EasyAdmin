# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-04-10 02:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EasyAdmin', '0003_auto_20180410_1018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='url',
            field=models.CharField(max_length=64, null=True, verbose_name='URL地址'),
        ),
    ]