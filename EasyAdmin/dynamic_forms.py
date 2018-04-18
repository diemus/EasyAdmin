from django import forms
from django.forms import ValidationError
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField

def modelform_factory(model_class,admin_class=None):
    attrs = {}

    class Meta:
        model=model_class
        fields="__all__"
        # exclude=['last_login']
        # if admin_class and admin_class.readonly_fields:
        #     exclude.extend(admin_class.readonly_fields)
    attrs['Meta']=Meta

    _model_form_class=type('DynamicModelForm',(forms.ModelForm,),attrs)
    return _model_form_class
