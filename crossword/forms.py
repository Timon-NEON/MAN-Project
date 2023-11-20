from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django.forms.widgets import Textarea
from django.http import HttpResponse
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

from .constants import language_template_choices

status_choices = (
    ('0', 'Open'),
    ('1', 'Clear'),
    ('2', 'Hiden')
    )


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=64, required=True)
    second_name = forms.CharField(max_length=64, required=True)
    email = forms.EmailField(max_length=128)
    class Meta:
        model = User
        fields=['username', 'first_name', 'second_name', 'email', 'password1', 'password2',]


class PostingForm(forms.Form):
    status = forms.ChoiceField(choices=status_choices)
    language = forms.ChoiceField(choices=language_template_choices)


class NewCrosswordForm(forms.Form):
    name = forms.CharField(label='')
    words = forms.CharField(label='', widget=Textarea(
        attrs={'placeholder': 'Слова кросворду', 'rows': 10, 'id': 'textar'}), required=False)
    time = forms.DecimalField(min_value=3, max_value=300)


class DemoCrosswordForm(forms.Form):
    name = forms.CharField(label='', disabled=True, required=False)
    words = forms.CharField(label='', widget=Textarea(
        attrs={'placeholder': 'Слова кросворду', 'rows': 10, 'id': 'textar'}), required=False, disabled=True)


class DrawForm(forms.Form):
    quality_choices = (
    (5, 'Low'),
    (10, 'Medium'),
    (20, 'Big')
    )
    quality = forms.ChoiceField(choices=quality_choices)


class SearchForm(forms.Form):
    ask = forms.CharField(label='', required=False, widget=forms.TextInput(attrs={'placeholder': 'Crossword\'s name'}))
    creator = forms.CharField(label='', required=False, widget=forms.TextInput(attrs={'placeholder': 'Creator'}))
    language = forms.ChoiceField(choices=(('##', 'All'),)  + language_template_choices)
    status = forms.ChoiceField(choices=(('##', 'All'),) + status_choices)
