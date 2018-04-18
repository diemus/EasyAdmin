"""CRM URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView
from EasyAdmin import views

urlpatterns = [
    url(r'^admin', admin.site.urls),
    url('^$', views.TableViews.as_view(),name='tables'),
    url('^(?P<app_name>[a-zA-Z0-9]+)$', views.ModelsViews.as_view(),name='app_models'),
    url('^(?P<app_name>[a-zA-Z0-9]+)/(?P<model_name>[a-zA-Z0-9]+)$', views.TableDataView.as_view(),name='table_data'),
    url('^(?P<app_name>[a-zA-Z0-9]+)/(?P<model_name>[a-zA-Z0-9]+)/param.js$', views.TableParamsView.as_view(),name='table_params'),
    url('^(?P<app_name>[a-zA-Z0-9]+)/(?P<model_name>[a-zA-Z0-9]+)/add$', views.AddView.as_view(),name='add'),
    url('^(?P<app_name>[a-zA-Z0-9]+)/(?P<model_name>[a-zA-Z0-9]+)/delete$', views.DeleteView.as_view(),name='delete'),
    url('^(?P<app_name>[a-zA-Z0-9]+)/(?P<model_name>[a-zA-Z0-9]+)/edit', views.EditView.as_view(),name='edit'),
    url('^menu_management$', views.MenuManagementView.as_view(),name='menu_management'),
]
