from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django.forms.widgets import Textarea
from django.http import HttpResponse
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=64, required=True)
    second_name = forms.CharField(max_length=64, required=True)
    email = forms.EmailField(max_length=128)
    class Meta:
        model = User
        fields=['username', 'first_name', 'second_name', 'email', 'password1', 'password2',]

class NewCrosswordForm(forms.Form):
    name = forms.CharField(label='')
    words = forms.CharField(label='', widget=Textarea(
        attrs={'placeholder': 'Слова кросворду', 'rows': 10, 'id': 'textar'}), required=False)
    time = forms.DecimalField(min_value=1, max_value=300)

class DemoCrosswordForm(forms.Form):
    name = forms.CharField(label='', disabled=True, required=False)
    words = forms.CharField(label='', widget=Textarea(
        attrs={'placeholder': 'Слова кросворду', 'rows': 10, 'id': 'textar'}), required=False, disabled=True)

class SignUpView(CreateView):
    form_class = SignUpForm    
    success_url = reverse_lazy('main:login')
    template_name = 'registration/registration.html'

class DrawForm(forms.Form):
    CHOICES = (
    (5, 'Low'),
    (10, 'Medium'),
    (20, 'Big')
    )
    quality = forms.ChoiceField(choices=CHOICES)