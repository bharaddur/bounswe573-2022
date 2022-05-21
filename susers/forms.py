from django import forms
from pods.models import Pod, Discussion

class PodEnrollForm(forms.Form):
    pod = forms.ModelChoiceField(queryset=Pod.objects.all(),widget=forms.HiddenInput)

class DiscussionForm(forms.ModelForm):
    class Meta:
        model = Discussion
        fields = ('title', 'body')

        Widgets = {
            'Title': forms.TextInput(),
            'Body': forms.Textarea(),
        }