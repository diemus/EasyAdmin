# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-04-11 12:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EasyAdmin', '0019_auto_20180411_2047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='order',
            field=models.PositiveSmallIntegerField(default=99, verbose_name='顺序'),
        ),
    ]
