# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-04-10 02:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('EasyAdmin', '0002_remove_user_roles'),
    ]

    operations = [
        migrations.CreateModel(
            name='MenuCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=32)),
            ],
            options={
                'verbose_name': '菜单分类',
                'verbose_name_plural': '菜单分类',
            },
        ),
        migrations.RemoveField(
            model_name='menu',
            name='name',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='url_name',
        ),
        migrations.AddField(
            model_name='menu',
            name='caption',
            field=models.CharField(default=1, max_length=32, verbose_name='标题'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='menu',
            name='has_submenu',
            field=models.BooleanField(default=False, verbose_name='是否拥有子菜单'),
        ),
        migrations.AddField(
            model_name='menu',
            name='icon_class',
            field=models.CharField(default='1', max_length=32, verbose_name='图表类'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='menu',
            name='parent_menu',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_menu', to='EasyAdmin.Menu', verbose_name='父菜单'),
        ),
        migrations.AddField(
            model_name='menu',
            name='url',
            field=models.CharField(default='', max_length=64, verbose_name='URL地址'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='menu',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='EasyAdmin.MenuCategory', verbose_name='菜单分类'),
            preserve_default=False,
        ),
    ]