from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone

# Create your models here.
class Customer(models.Model):
    '''客户信息表'''
    name=models.CharField('姓名',max_length=32,blank=True,null=True)
    qq=models.CharField('QQ',max_length=64,unique=True)
    qq_name=models.CharField('QQ名',max_length=64,blank=True,null=True)
    mobile=models.CharField('手机号',max_length=32)
    id_num=models.CharField('身份证号',max_length=64,blank=True,null=True)
    email=models.EmailField('邮箱',max_length=64,blank=True,null=True)
    source_choices = ((0,'转介绍'),
                      (1,'QQ群'),
                      (2,'官网'),
                      (3,'百度推广'),
                      (4,'51CTO'),
                      (5,'知乎'),
                      (6,'市场推广')
                      )
    source=models.PositiveSmallIntegerField('来源',choices=source_choices)
    referral_from = models.CharField(verbose_name="转介绍人qq", max_length=64, blank=True, null=True)
    consult_course = models.ForeignKey("Course",verbose_name="咨询课程")
    content = models.TextField(verbose_name="咨询详情")
    tags = models.ManyToManyField("Tag",blank=True)
    status_choices = ((0,'未报名'),
                      (1,'已报名'),
                      )
    status = models.SmallIntegerField(choices=status_choices,default=1)
    consultant = models.ForeignKey('User',verbose_name='咨询顾问')
    memo = models.TextField(blank=True,null=True)
    ctime = models.DateTimeField(auto_now_add=True,verbose_name='创建日期')

    def __str__(self):
        return self.name if self.name else self.qq

    class Meta:
        verbose_name ="客户表"
        verbose_name_plural ="客户表"
        ordering=['id']

class Tag(models.Model):
    name = models.CharField(unique=True,max_length=32)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = "标签"


class CustomerFollowUp(models.Model):
    '''客户跟进记录'''
    customer=models.ForeignKey('Customer')
    content=models.TextField(verbose_name='跟进内容')
    consultant=models.ForeignKey('User')
    intention_choices  = ((0,'2周内报名'),
                          (1,'1个月内报名'),
                          (2,'近期无报名计划'),
                          (3,'已在其它机构报名'),
                          (4,'已报名'),
                          (5,'已拉黑'),
                          )
    intention = models.SmallIntegerField(choices=intention_choices)
    ctime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "<%s : %s>" %(self.customer.qq,self.intention)

    class Meta:
        verbose_name = "客户跟进记录"
        verbose_name_plural = "客户跟进记录"

class Course(models.Model):
    '''课程表'''
    name = models.CharField(max_length=64,unique=True)
    price = models.PositiveSmallIntegerField()
    period = models.PositiveSmallIntegerField(verbose_name="周期(月)")
    outline = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "课程表"
        verbose_name_plural = "课程表"

class Enrollment(models.Model):
    '''报名表'''
    customer = models.ForeignKey("Customer")
    enrolled_class = models.ForeignKey("ClassList",verbose_name="所报班级",null=True)
    consultant = models.ForeignKey("User",verbose_name="课程顾问",null=True)
    contract_agreed = models.BooleanField(default=False,verbose_name="学员已同意合同条款")
    contract_approved = models.BooleanField(default=False,verbose_name="合同已审核")
    status = models.BooleanField(default=False,verbose_name="报名状态")
    ctime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s" %(self.customer,self.enrolled_class)

    class Meta:
        unique_together = ("customer","enrolled_class")
        verbose_name_plural = "报名表"

class Payment(models.Model):
    '''缴费记录'''
    enrollment = models.ForeignKey("Enrollment")
    amount = models.PositiveIntegerField(verbose_name="数额")
    ctime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s %s" %(self.enrollment.customer.name,self.enrollment.enrolled_class.course.name,self.amount)

    class Meta:
        verbose_name_plural = "缴费记录"

class Branch(models.Model):
    '''校区'''
    name = models.CharField(max_length=128,unique=True)
    addr = models.CharField(max_length=128)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "校区"
        verbose_name_plural = "校区"

class ContractTemplate(models.Model):
    name=models.CharField('合同名称',max_length=64,unique=True)
    template=models.TextField('合同模板')

    def __str__(self):
        return self.name

class ClassList(models.Model):
    '''班级表'''
    branch = models.ForeignKey("Branch",verbose_name="校区")
    course = models.ForeignKey("Course")
    class_type_choices = ((0,'面授(脱产)'),
                          (1,'面授(周末)'),
                          (2,'网络班')
                          )
    class_type = models.SmallIntegerField(choices=class_type_choices,verbose_name="班级类型")
    semester = models.PositiveSmallIntegerField(verbose_name="学期")
    teachers = models.ManyToManyField('User',blank=True)
    contract=models.ForeignKey(to='ContractTemplate',blank=True,null=True)
    start_date = models.DateField(verbose_name="开班日期")
    end_date = models.DateField(verbose_name="结业日期",blank=True,null=True)

    def __str__(self):
        return "%s %s %s" %(self.branch,self.course,self.semester)

    class Meta:
        unique_together = ('branch','course','semester')
        verbose_name_plural = "班级"
        verbose_name = "班级"

class CourseRecord(models.Model):
    '''上课记录表'''
    from_class = models.ForeignKey("ClassList",verbose_name="班级")
    day_num = models.PositiveSmallIntegerField(verbose_name="第几节(天)")
    teacher = models.ForeignKey('User')
    has_homework = models.BooleanField(default=True)
    homework_title = models.CharField(max_length=128,blank=True,null=True)
    homework_content = models.TextField(blank=True,null=True)
    outline = models.TextField(verbose_name="本节课程大纲")
    ctime = models.DateField(auto_now_add=True)

    def __str__(self):
        return "%s %s" %(self.from_class,self.day_num)

    class Meta:
        unique_together = ("from_class", "day_num")
        verbose_name_plural = "上课记录"

class StudyRecord(models.Model):
    '''学习记录表'''
    student = models.ForeignKey("Enrollment")
    course_record = models.ForeignKey("CourseRecord")
    attendance_choices = ((0,'已签到'),
                          (1,'迟到'),
                          (2,'缺勤'),
                          (3,'早退'),
                          )
    attendance = models.SmallIntegerField(choices=attendance_choices,default=0)
    score_choices = ((100,"A+"),
                     (90,"A"),
                     (85,"B+"),
                     (80,"B"),
                     (75,"B-"),
                     (70,"C+"),
                     (60,"C"),
                     (40,"C-"),
                     (-50,"D"),
                     (-100,"COPY"),
                     (0,"N/A"),
                     )
    score = models.SmallIntegerField(choices=score_choices,default=0)
    memo = models.TextField(blank=True,null=True)
    ctime = models.DateField(auto_now_add=True)

    def __str__(self):
        return "%s %s %s" %(self.student,self.course_record,self.score)

    class Meta:
        unique_together = ('student','course_record')
        verbose_name_plural = "学习记录"

class Role(models.Model):
    '''角色表'''
    name = models.CharField(max_length=32,unique=True)
    menus = models.ManyToManyField("Menu",blank=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "角色"


class Menu(models.Model):
    '''菜单'''
    caption = models.CharField('标题',max_length=32,default='',blank=True)
    icon_class = models.CharField('图标类',max_length=32,default='',blank=True)
    url = models.CharField('URL地址',max_length=64,default='',blank=True)
    url_names = models.CharField('URL Name',max_length=64,default='',blank=True)
    has_submenu=models.BooleanField('是否拥有子菜单',default=False)
    parent_menu=models.ForeignKey(verbose_name='父菜单',to='Menu',related_name='sub_menu',null=True)
    order=models.PositiveSmallIntegerField('顺序',default=99)


    def __str__(self):
        return self.caption

    @property
    def level(self):
        menu=self
        level=0
        while menu.parent_menu:
            menu=menu.parent_menu
            level+=1
        return level

    def get_url_names(self):
        return self.url_names.split(',') if self.url_names else []


    class Meta:
        verbose_name='菜单配置'
        verbose_name_plural = verbose_name
        ordering=['order']
        # unique_together=[
        #     ('order','parent_menu')
        # ]

class UserManager(BaseUserManager):
    def _create_user(self, email, name, password, **extra_fields):
        if not email:
            raise ValueError('邮箱不能为空！')
        if not name:
            raise ValueError('姓名不能为空！')
        email = self.normalize_email(email)
        user = self.model(name=name, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, name, password, **extra_fields)

    def create_superuser(self, email, name, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, name, password, **extra_fields)

class User(AbstractBaseUser,PermissionsMixin):

    email = models.EmailField('邮箱',max_length=255,unique=True)
    name = models.CharField('姓名',max_length=32)
    avatar=models.CharField('头像',max_length=256,default='/static/img/profile-photos/1.png')
    is_staff = models.BooleanField('是否为员工',default=False)
    is_active = models.BooleanField('账户状态',default=True)
    ctime = models.DateTimeField('注册时间',default=timezone.now)
    student = models.ForeignKey("Customer", verbose_name="关联学员账号", blank=True, null=True,
                                    help_text="只有学员报名后方可为其创建账号")

    password = models.CharField('密码', max_length=128)
    last_login = models.DateTimeField('最后登录时间', blank=True, null=True)


    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        verbose_name='用户信息'
        verbose_name_plural='用户信息'
        permissions=[
            ('global_password_change','有权修改任意账户密码'),
        ]

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self._meta.get_field('is_superuser').verbose_name = "是否为管理员"
        self._meta.get_field('is_superuser').help_text = "管理员账户拥有所有权限"
        self._meta.get_field('groups').verbose_name = "用户组"
        self._meta.get_field('groups').help_text = "该用户将拥有用户所在组的所有权限"
        self._meta.get_field('user_permissions').verbose_name = "用户权限"
        self._meta.get_field('user_permissions').help_text = "该用户所拥有的权限"

    def clean(self):
        super(User, self).clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        # The user is identified by their email address
        return self.name

    def get_short_name(self):
        # The user is identified by their email address
        return self.name

    def __str__(self):
        return self.email