import re

from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm

from .models import Question


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['text','imagepath','imagepath','topic']
