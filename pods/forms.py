from django import forms
from django.forms.models import inlineformset_factory
from .models import Pod, Module

ModuleFormSet = inlineformset_factory(Pod, Module, fields=['title','description'], extra=2, can_delete=True)