from collections import OrderedDict
from bs4 import BeautifulSoup
import json
def build_menu_list(queryset):

    menu_dict=OrderedDict()
    for obj in queryset.order_by('order'):
        menu_dict[obj.id]={
            'id':obj.id,
            'caption':obj.caption,
            'icon_class':obj.icon_class,
            'url':obj.url,
            'url_names':obj.get_url_names(),
            'parent_menu_id':obj.parent_menu_id,
            'parent_menu_obj':obj.parent_menu,
            'obj':obj,
            'order':obj.order,
            'submenu': [],
        }
    # 构造多级菜单字典
    result_list=[]
    for k,v in menu_dict.items():
        pid=v['parent_menu_id']
        if pid:
            menu_dict[pid]['submenu'].append(v)
        else:
            result_list.append(v)
    return result_list

def build_new_menu_ele(obj):
    soup = BeautifulSoup('', 'lxml')
    dd_item = soup.new_tag('li', **{
        'class': 'dd-item',
        'data-id': obj.id,
        'data-caption': obj.caption,
        'data-icon_class': obj.icon_class,
        'data-url': obj.url,
        'data-url_names': obj.url_names,
    })
    # dd-hanle
    dd_handle = soup.new_tag('div', **{'class': 'dd-handle'})
    dd_item.append(dd_handle)
    span = soup.new_tag('span', **{'class': 'menu-caption'})
    span.append(obj.caption)
    dd_handle.append(span)

    # 处理图标
    icon = soup.new_tag('i', **{'class': obj.icon_class, 'style': 'padding-right: 10px'})
    dd_handle.insert(0, icon)

    return dd_item
