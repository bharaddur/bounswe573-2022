from django import forms
from pods.models import Pod

class PodEnrollForm(forms.Form):
    pod = forms.ModelChoiceField(queryset=Pod.objects.all(),widget=forms.HiddenInput)