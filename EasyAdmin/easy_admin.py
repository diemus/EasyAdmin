from django.contrib import admin
from EasyAdmin import models
# Register your models here.
enabled_admins = {}

def register(model_cls,admin_cls=None):

    if model_cls._meta.app_label not in enabled_admins:
        enabled_admins[model_cls._meta.app_label]={}

    enabled_admins[model_cls._meta.app_label][model_cls._meta.model_name]=admin_cls
    admin_cls.model = model_cls
    # if admin_cls is not None:
    #     # 判断list_display是否包含主键，并将主键设为第一列
    #     if model_cls._meta.pk.name in admin_cls.list_display:
    #         admin_cls.list_display.remove(model_cls._meta.pk.name)
    #         admin_cls.list_display.insert(0,model_cls._meta.pk.name)
    #     else:
    #         admin_cls.list_display.insert(0, model_cls._meta.pk.name)
    #
    #     enabled_admins[model_cls._meta.app_label][model_cls._meta.model_name].update({'EasyAdmin':admin_cls})
    #
    #     # 如果未设置搜索字段，则将主键设为搜索字段
    #     if not admin_cls.search_fields:
    #         admin_cls.search_fields.insert(0, model_cls._meta.pk.name)
    #
    #     # 判断是否设置了ordering
    #     if not admin_cls.ordering:
    #         admin_cls.ordering=[model_cls._meta.pk.name]
    #
    #     # 整表只读时，保险起见将所有字段设为只读
    #     if admin_cls.readonly_table:
    #         all_fields=model_cls._meta.local_fields+model_cls._meta.local_many_to_many
    #         admin_cls.readonly_fields=[field.name for field in all_fields]
    #
    #     # 未设置fieldset时，默认显示所有字段
    #     if not admin_cls.fieldsets:
    #         all_fields = model_cls._meta.local_fields + model_cls._meta.local_many_to_many
    #         admin_cls.fieldsets=(
    #             (None,{'fields':[field.name for field in all_fields]}),
    #         )
    #
    #
    #     # 将model赋值给admin
    #     admin_cls.model=model_cls

class CustomerAdmin:
    list_display = ['id','qq','name','source','consultant','consult_course','ctime','status','enroll']
    list_filters = ['name','source','consultant','consult_course','status','ctime']
    search_fields = ['qq', 'name', "consultant__name"]
    filter_horizontal = ['tags']
    ordering = ['id']
    readonly_fields = ['qq','consultant','tags']
    readonly_table = False

    def enroll(self,obj):
        url=''
        ele='<a href="%s">报名</a>'%url
        return ele
    enroll.verbose_name='报名链接'

register(models.Customer,CustomerAdmin)