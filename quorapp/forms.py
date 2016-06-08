import re

from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm

from .models import Topic

class UserProfileForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        sex_choices = (
            ('M', 'Male'),
            ('F', 'Female'),
        )
        self.fields['first_name'] = forms.CharField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Fist Name"))
        self.fields['last_name'] = forms.CharField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Last Name"))
        self.fields['profileimage'] = forms.CharField(widget=forms.TextInput(attrs=dict(max_length=200)), label=_("Profile Image"))
        self.fields['about'] = forms.CharField(widget=forms.TextInput(attrs=dict(max_length=200)), label=_("About"))
        self.fields['age'] = forms.CharField(max_length=3, label=_("Age"))
        self.fields['sex'] = forms.ChoiceField(choices = sex_choices, label=_("Sex"))
        self.fields['website'] = forms.CharField(widget=forms.TextInput(attrs=dict(max_length=200)), label=_("Website"))


class QuestionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)

        topic_choices = [(topic.id, topic.name) for topic in Topic.objects.all()]
        self.fields['topics'] = forms.ChoiceField(choices = topic_choices, label=_("topic"), required = True)
        self.fields['text'] = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Please enter the question'}),max_length=10000,required = True, label=_("text"))


class AnswerForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)
        self.fields['text'] = forms.CharField(widget=forms.Textarea(
            attrs={'placeholder': 'Please enter the answer'}),
            max_length=10000,
            required=True,
            label=_("text")
            )
        self.fields['imagepath'] = forms.CharField(
            widget=forms.TextInput(),
            max_length=200, label=_("imagepath"),
            required=False
            )


class CommentForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['text'] = forms.CharField(widget=forms.Textarea(
            attrs={'placeholder': 'Please enter the comment'}),
            max_length=10000,
            required=True,
            label=_("text")
            )


class DeletePostForm(forms.Form):
    pass


class FollowForm(forms.Form):
    pass


class UpvotesForm(forms.Form):
    pass


class SeekForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(SeekForm, self).__init__(*args, **kwargs)
        self.fields['search'] = forms.CharField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Username"))


class SeekConfirmForm(forms.Form):
    pass
