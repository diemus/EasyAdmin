# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-04-05 15:16
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('addr', models.CharField(max_length=128)),
            ],
            options={
                'verbose_name': '校区',
                'verbose_name_plural': '校区',
            },
        ),
        migrations.CreateModel(
            name='ClassList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_type', models.SmallIntegerField(choices=[(0, '面授(脱产)'), (1, '面授(周末)'), (2, '网络班')], verbose_name='班级类型')),
                ('semester', models.PositiveSmallIntegerField(verbose_name='学期')),
                ('start_date', models.DateField(verbose_name='开班日期')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='结业日期')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EasyAdmin.Branch', verbose_name='校区')),
            ],
            options={
                'verbose_name': '班级',
                'verbose_name_plural': '班级',
            },
        ),
        migrations.CreateModel(
            name='ContractTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='合同名称')),
                ('template', models.TextField(verbose_name='合同模板')),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('price', models.PositiveSmallIntegerField()),
                ('period', models.PositiveSmallIntegerField(verbose_name='周期(月)')),
                ('outline', models.TextField()),
            ],
            options={
                'verbose_name': '课程表',
                'verbose_name_plural': '课程表',
            },
        ),
        migrations.CreateModel(
            name='CourseRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_num', models.PositiveSmallIntegerField(verbose_name='第几节(天)')),
                ('has_homework', models.BooleanField(default=True)),
                ('homework_title', models.CharField(blank=True, max_length=128, null=True)),
                ('homework_content', models.TextField(blank=True, null=True)),
                ('outline', models.TextField(verbose_name='本节课程大纲')),
                ('ctime', models.DateField(auto_now_add=True)),
                ('from_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EasyAdmin.ClassList', verbose_name='班级')),
            ],
            options={
                'verbose_name_plural': '上课记录',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=32, null=True, verbose_name='姓名')),
                ('qq', models.CharField(max_length=64, unique=True, verbose_name='QQ')),
                ('qq_name', models.CharField(blank=True, max_length=64, null=True, verbose_name='QQ名')),
                ('mobile', models.CharField(max_length=32, verbose_name='手机号')),
                ('id_num', models.CharField(blank=True, max_length=64, null=True, verbose_name='身份证号')),
                ('email', models.EmailField(blank=True, max_length=64, null=True, verbose_name='邮箱')),
                ('source', models.PositiveSmallIntegerField(choices=[(0, '转介绍'), (1, 'QQ群'), (2, '官网'), (3, '百度推广'), (4, '51CTO'), (5, '知乎'), (6, '市场推广')], verbose_name='来源')),
                ('referral_from', models.CharField(blank=True, max_length=64, null=True, verbose_name='转介绍人qq')),
                ('content', models.TextField(verbose_name='咨询详情')),
                ('status', models.SmallIntegerField(choices=[(0, '未报名'), (1, '已报名')], default=1)),
                ('memo', models.TextField(blank=True, null=True)),
                ('ctime', models.DateTimeField(auto_now_add=True, verbose_name='创建日期')),
                ('consult_course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EasyAdmin.Course', verbose_name='咨询课程')),
            ],
            options={
                'verbose_name': '客户表',
                'verbose_name_plural': '客户表',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='CustomerFollowUp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='跟进内容')),
                ('intention', models.SmallIntegerField(choices=[(0, '2周内报名'), (1, '1个月内报名'), (2, '近期无报名计划'), (3, '已在其它机构报名'), (4, '已报名'), (5, '已拉黑')])),
                ('ctime', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': '客户跟进记录',
                'verbose_name_plural': '客户跟进记录',
            },
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract_agreed', models.BooleanField(default=False, verbose_name='学员已同意合同条款')),
                ('contract_approved', models.BooleanField(default=False, verbose_name='合同已审核')),
                ('status', models.BooleanField(default=False, verbose_name='报名状态')),
                ('ctime', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': '报名表',
            },
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('url_name', models.CharField(max_length=64)),
            ],
            options={
                'verbose_name': '菜单配置',
                'verbose_name_plural': '菜单配置',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField(verbose_name='数额')),
                ('ctime', models.DateTimeField(auto_now_add=True)),
                ('enrollment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EasyAdmin.Enrollment')),
            ],
            options={
                'verbose_name_plural': '缴费记录',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True)),
                ('menus', models.ManyToManyField(blank=True, to='EasyAdmin.Menu')),
            ],
            options={
                'verbose_name_plural': '角色',
            },
        ),
        migrations.CreateModel(
            name='StudyRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attendance', models.SmallIntegerField(choices=[(0, '已签到'), (1, '迟到'), (2, '缺勤'), (3, '早退')], default=0)),
                ('score', models.SmallIntegerField(choices=[(100, 'A+'), (90, 'A'), (85, 'B+'), (80, 'B'), (75, 'B-'), (70, 'C+'), (60, 'C'), (40, 'C-'), (-50, 'D'), (-100, 'COPY'), (0, 'N/A')], default=0)),
                ('memo', models.TextField(blank=True, null=True)),
                ('ctime', models.DateField(auto_now_add=True)),
                ('course_record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EasyAdmin.CourseRecord')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EasyAdmin.Enrollment')),
            ],
            options={
                'verbose_name_plural': '学习记录',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True)),
            ],
            options={
                'verbose_name': '标签',
                'verbose_name_plural': '标签',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_superuser', models.BooleanField(default=False, help_text='管理员账户拥有所有权限', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='邮箱')),
                ('name', models.CharField(max_length=32, verbose_name='姓名')),
                ('is_staff', models.BooleanField(default=False, verbose_name='是否为员工')),
                ('is_active', models.BooleanField(default=True, verbose_name='账户状态')),
                ('ctime', models.DateTimeField(default=django.utils.timezone.now, verbose_name='注册时间')),
                ('password', models.CharField(max_length=128, verbose_name='密码')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='最后登录时间')),
                ('groups', models.ManyToManyField(blank=True, help_text='该用户将拥有用户所在组的所有权限', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('roles', models.ManyToManyField(blank=True, to='EasyAdmin.Role')),
                ('student', models.ForeignKey(blank=True, help_text='只有学员报名后方可为其创建账号', null=True, on_delete=django.db.models.deletion.CASCADE, to='EasyAdmin.Customer', verbose_name='关联学员账号')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='该用户所拥有的权限', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': '用户信息',
                'verbose_name_plural': '用户信息',
                'permissions': [('global_password_change', '有权修改任意账户密码')],
            },
        ),
        migrations.AddField(
            model_name='enrollment',
            name='consultant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='课程顾问'),
        ),
        migrations.AddField(
            model_name='enrollment',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EasyAdmin.Customer'),
        ),
        migrations.AddField(
            model_name='enrollment',
            name='enrolled_class',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='EasyAdmin.ClassList', verbose_name='所报班级'),
        ),
        migrations.AddField(
            model_name='customerfollowup',
            name='consultant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='customerfollowup',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EasyAdmin.Customer'),
        ),
        migrations.AddField(
            model_name='customer',
            name='consultant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='咨询顾问'),
        ),
        migrations.AddField(
            model_name='customer',
            name='tags',
            field=models.ManyToManyField(blank=True, to='EasyAdmin.Tag'),
        ),
        migrations.AddField(
            model_name='courserecord',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='classlist',
            name='contract',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='EasyAdmin.ContractTemplate'),
        ),
        migrations.AddField(
            model_name='classlist',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EasyAdmin.Course'),
        ),
        migrations.AddField(
            model_name='classlist',
            name='teachers',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='studyrecord',
            unique_together=set([('student', 'course_record')]),
        ),
        migrations.AlterUniqueTogether(
            name='enrollment',
            unique_together=set([('customer', 'enrolled_class')]),
        ),
        migrations.AlterUniqueTogether(
            name='courserecord',
            unique_together=set([('from_class', 'day_num')]),
        ),
        migrations.AlterUniqueTogether(
            name='classlist',
            unique_together=set([('branch', 'course', 'semester')]),
        ),
    ]