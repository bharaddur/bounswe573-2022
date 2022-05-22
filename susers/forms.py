from django import forms
from pods.models import Pod, Discussion, Comment

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

class CommentForm (forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'md-textarea form-control',
        'placeholder': 'comment here...',
        'rows': '4',
    }))

    class Meta:
        model = Comment
        fields = ('body',)