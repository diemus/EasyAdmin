from django.shortcuts import render,reverse,HttpResponse
from EasyAdmin.easy_admin import enabled_admins
# Create your views here.
from django.views.generic import TemplateView,ListView,View,CreateView,UpdateView
from django.views.generic.base import ContextMixin
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator,EmptyPage
from django.core.exceptions import FieldDoesNotExist
from django.db.models import Q
from django.db.models import Model
from django.contrib.contenttypes.models import ContentType
from EasyAdmin.dynamic_forms import modelform_factory
from django.apps import apps
from django.http import QueryDict
from EasyAdmin import models
from EasyAdmin.utils import build_menu_list,build_new_menu_ele
from django_bulk_update.helper import bulk_update
import json

class BaseMixin(ContextMixin):

    def get_context_data(self, **kwargs):
        context = super(BaseMixin, self).get_context_data(**kwargs)

        # 获取菜单列表
        queryset=models.Menu.objects.prefetch_related()
        context['menu_list']=build_menu_list(queryset)
        return context

class ModelAdminMixin(BaseMixin,View):
    admin=None
    model=None

    def dispatch(self, request, *args, **kwargs):
        self.app_name=self.kwargs.get('app_name')
        self.model_name=self.kwargs.get('model_name')
        if self.app_name and self.model_name:
            self.admin = enabled_admins[self.app_name][self.model_name]
            self.model = self.admin.model
        return super(ModelAdminMixin,self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ModelAdminMixin, self).get_context_data(**kwargs)
        context['breadcrumb']=[
            {'label':'Home','url':reverse('tables')}
        ]
        if self.app_name:
            context['app_name']=self.app_name
            context['app_label']=apps.get_app_config(self.app_name).verbose_name
            context['breadcrumb'].append({
                'label': context['app_label'],
                'url': reverse('app_models',kwargs={'app_name':self.app_name})
            })
        if self.model_name:
            context['model_name']=self.model_name
            context['model_label']=self.model._meta.verbose_name
            context['admin_cls'] = self.admin
            context['breadcrumb'].append({
                'label': context['model_label'],
                'url': reverse('table_data',kwargs={'app_name':self.app_name,'model_name':self.model_name})
            })
        return context

class TableViews(ModelAdminMixin,TemplateView):
    template_name = 'tables.html'

    def get_context_data(self, **kwargs):
        context = super(TableViews, self).get_context_data(**kwargs)
        context['table_list']=enabled_admins
        context['page_title']='数据库管理系统'
        return context

class ModelsViews(ModelAdminMixin,TemplateView):
    template_name = 'tables.html'

    def get_context_data(self, **kwargs):
        context = super(ModelsViews, self).get_context_data(**kwargs)
        context['table_list']={
            self.app_name:enabled_admins[self.app_name]
        }
        context['page_title']='模型列表'
        return context

class TableDataView(ModelAdminMixin,TemplateView):
    template_name = 'table_data.html'

    def get_context_data(self, **kwargs):
        context = super(TableDataView, self).get_context_data(**kwargs)
        context['page_title']='数据表'
        return context

    def post(self, request, *args, **kwargs):
        '''Ajax请求处理，返回JSON数据'''
        # 获取POST参数
        limit=int(self.request.POST.get('limit'))       # 每页显示数量
        offset=int(self.request.POST.get('offset'))     #页数=offset//limit+1
        order='' if self.request.POST.get('order')=='asc' else '-'
        search=self.request.POST.get('search',None)          # 搜索字段，可能为None
        sort=self.request.POST.get('sort','pk')              # 排序字段，可能为None
        filter=self.request.POST.get('filter',{})          # 过滤字段，可能为None


        # 搜索条件
        q_search = Q()
        if search:
            q_search.connector = 'OR'
            for field in self.admin.search_fields:
                q_search.children.append(("%s__contains" % field, search))

        # 过滤条件
        if filter:
            filter=json.loads(filter)
            for k,v in filter.items():
                if v=='null':          # 处理值为None的情况
                    del filter[k]
                    filter['%s__isnull'%k]=True
        # print(filter)
        # 排序条件
        ordering=order+sort

        queryset = self.admin.model.objects.filter(q_search,**filter).prefetch_related().order_by(ordering)
        p = Paginator(queryset, limit)

        # 生成Bootstrap Table需要的Json数据格式
        data={
            'total':queryset.count(),
            'rows':[],
        }

        try:
            object_list=p.page(offset//limit+1).object_list
        except EmptyPage:
            object_list=[]

        for obj in p.page(offset//limit+1).object_list:
            row={}
            for field_name in self.admin.list_display:
                row[field_name]=get_data_by_field(obj,field_name,self.admin)
            data['rows'].append(row)
        return HttpResponse(json.dumps(data))

class TableParamsView(ModelAdminMixin,View):
    '''
    根据Model及Admin配置，动态生成Bootstrap-Table所需要的参数，并以
    页面加载script的方式将变量ParamsForBootstrapTable直接放入浏览器
    '''

    def get(self,request,*args,**kwargs):
        # 获取filter条件
        queryset = self.admin.model.objects.prefetch_related()

        field_list=[]
        # 表头部分的checkbox
        field_list.append({
            'checkbox': True,
            'align': 'center',
            'valign': 'middle',
        })
        for field_name in self.admin.list_display:
            try:
                field=self.admin.model._meta.get_field(field_name)
                params=get_filter_by_field(queryset,field)
            except FieldDoesNotExist:
                # admin中的自定义字段
                field=getattr(self.admin,field_name)
                params = None
            finally:

                field_info={
                    'field':field_name,
                    'title':field.verbose_name.upper(),
                    'sortable':True,
                    'valign':'middle',
                    'visible':True,
                    'searchable':True,
                    'escape':False,
                }
                if params:field_info.update(params)
                field_list.append(field_info)
        # 添加结尾按钮
        field_list.append({
            'field': 'operate',
            'title': '操作',
            'align':'center',
            'valign': 'middle',
            'clickToSelect':False,
            'events': 'operateEvents',
            'formatter': 'operateFormatter',
        })
        json_params=json.dumps(field_list,ensure_ascii=False)
        return HttpResponse('var ParamsForBootstrapTable=%s'%json_params)

def get_data_by_field(model_obj,field_name,admin_class=None):
    try:
        field_obj = model_obj._meta.get_field(field_name)
        result = getattr(model_obj, field_name)
        if field_obj.choices:
            result=getattr(model_obj,'get_%s_display'%field_name)()
        elif isinstance(result,Model):
            result=result.__str__()
        elif type(result).__name__=='datetime':
            result=result.strftime("%Y-%m-%d %H:%M:%S")
        elif result is True: result = '<span class="glyphicon glyphicon-ok"></span>'
        elif result is False: result = '<span class="glyphicon glyphicon-remove"></span>'
        else:
            result =field_obj.value_to_string(model_obj)

        return result
    except FieldDoesNotExist:
        # 自定义字段
        func=getattr(admin_class,field_name,None)
        if func:
            result=func(admin_class,model_obj)
            return result

def get_filter_by_field(queryset,field):
    # 暂时不启用
    if type(field).__name__ == "DateTimeField":
        dic={
            'format': 'mm/dd/yyyy',
            'language':'zh_CN'
        }

        params={
            'filterControl': 'datepicker',
            'filterDatepickerOptions':'',
        }
    else:
        result = queryset.values(field.name).distinct().order_by(field.name)
        dic={}
        for d in result:
            obj=queryset.filter(**d).first()
            value=get_data_by_field(obj,field.name)
            dic.update({
                d[field.name]:value
            })

        jso=json.dumps(dic,ensure_ascii=False)
        params={
            'filterControl': 'select',
            'filterData': 'json:%s'%jso,
        }
        # print(params)
    return params

class AddView(ModelAdminMixin,CreateView):
    template_name = 'edit.html'
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(AddView, self).get_context_data(**kwargs)
        context['page_title']='新增'
        return context

    def get_form_class(self):
        return modelform_factory(self.model,self.admin)

    def get_success_url(self):
        app_name=self.kwargs.get('app_name')
        model_name=self.kwargs.get('model_name')
        url=reverse('table_data',kwargs={'app_name':app_name,'model_name':model_name})
        return url

class EditView(ModelAdminMixin,UpdateView):
    template_name = 'edit.html'

    def get_context_data(self, **kwargs):
        context = super(EditView, self).get_context_data(**kwargs)
        context['page_title']='编辑'
        return context

    def get_form_class(self):
        return modelform_factory(self.model,self.admin)

    def get_object(self, queryset=None):
        pk=self.request.GET.get('pk')
        if not pk:
            pk=self.request.POST.get('pk')
        return self.model.objects.get(pk=pk)

    def get_success_url(self):
        app_name=self.kwargs.get('app_name')
        model_name=self.kwargs.get('model_name')
        url=reverse('table_data',kwargs={'app_name':app_name,'model_name':model_name})
        return url

class DeleteView(ModelAdminMixin,View):

    def post(self,request, *args, **kwargs):
        pk_list=request.POST.getlist('pk')
        queryset=self.model.objects.filter(pk__in=pk_list)
        rep_data={}
        try:
            queryset.delete()
            rep_data['status'] = True
        except Exception:
            rep_data['status']=False
        return HttpResponse(json.dumps(rep_data,ensure_ascii=False))

class MenuManagementView(BaseMixin,CreateView):
    template_name = 'menu_management.html'
    model = models.Menu
    fields = ['caption','icon_class','url','url_names']

    def get_context_data(self, **kwargs):
        context = super(MenuManagementView, self).get_context_data(**kwargs)
        queryset=models.Menu.objects.prefetch_related()
        context['all_menu_list']=build_menu_list(queryset)
        return context

    def form_valid(self, form):
        obj=form.save()
        # 未提供标题时，设置初始标题
        if not obj.caption:
            obj.caption='无标题'
            obj = form.save()
        rep_data={
            'status':True,
            'ele':build_new_menu_ele(obj).__str__(),
        }
        return HttpResponse(json.dumps(rep_data,ensure_ascii=False))

    def form_invalid(self, form):
        errors=json.loads(form.errors.as_json())
        rep_data={
            'status':False,
            'errors':errors,
        }
        return HttpResponse(json.dumps(rep_data,ensure_ascii=False))

    def delete(self,request,*args,**kwargs):
        rep_data={
            'status':True,
        }
        DELETE=QueryDict(self.request.body)
        id_list=DELETE.getlist('id')
        try:
            models.Menu.objects.filter(id__in=id_list).delete()
        except Exception as e:
            rep_data['status']=False
        return HttpResponse(json.dumps(rep_data,ensure_ascii=False))

    def put(self,request,*args,**kwargs):
        rep_data={
            'status':True,
        }
        menu_list = json.loads(self.request.body)
        # print(data)
        # try:
        result_list=[]
        queryset=models.Menu.objects.prefetch_related()
        self.build_menu_bulk_list(menu_list,queryset,result_list)
        # print(result_list)
        bulk_update(result_list)
            # obj.save()
        # except Exception as e:
        #     rep_data['status'] = False
        #     print(e)
        return HttpResponse(json.dumps(rep_data,ensure_ascii=False))

    def build_menu_bulk_list(self,menu_list,queryset,result_list,parent_menu=None):
        for n,menu in enumerate(menu_list):
            obj=queryset.get(id=int(menu['id']))
            obj.icon_class=menu['icon_class']
            obj.caption=menu['caption']
            obj.url=menu['url']
            obj.url_names=menu['url_names']
            obj.has_submenu=True if menu.get('children') else False
            obj.parent_menu_id=None if not parent_menu else int(parent_menu['id'])
            obj.order=n
            result_list.append(obj)

            if menu.get('children'):
                self.build_menu_bulk_list(menu['children'],queryset,result_list,parent_menu=menu)