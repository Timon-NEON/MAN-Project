from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from django.forms.widgets import Textarea
from django.http import HttpResponse

import random
import copy
import ast

from crossword.man_project.CW import Crossword

# Create your views here.

class NewCrosswordForm(forms.Form):
    name = forms.CharField(label='')
    words = forms.CharField(label='', widget=Textarea(
        attrs={'placeholder': 'Слова кросворду', 'rows': 10, 'id': 'textar'}), required=False)
    time = forms.DecimalField(min_value=1, max_value=300)

class DrawForm(forms.Form):
    CHOICES = (
    (5, 'Low'),
    (10, 'Medium'),
    (20, 'Big')
    )
    quality = forms.ChoiceField(choices=CHOICES)

    
def index(request):
    if 'ses_info' not in request.session:
        request.session['ses_info'] = {'describe': [], 'id':random.randint(1, 100000), 'form': None}
    response = render(request, 'crossword/index.html', {
        'form': NewCrosswordForm(),
        'ses_info': request.session['ses_info'],
    })
    response.set_cookie(key='id', value=str(random.randint(1, 100000)))
    response.set_cookie(key='name', value='')
    response.set_cookie(key='arr', value=[])
    response.set_cookie(key='describe', value={})
    response.set_cookie(key='text', value={})
    return response

def generate(request):
    if request.method == 'POST':
        form = NewCrosswordForm(request.POST)
        if form.is_valid():
            crossword = Crossword()
            name = form.cleaned_data['name']
            text = form.cleaned_data['words']
            time = form.cleaned_data['time']
            
            id = request.COOKIES.get('id')

            crossword.read(text)
            crossword.name = name
            crossword.generate(int(time))
            if crossword.best_crossword != []:
                crossword.draw(15, id, True)
                
                response = render(request, 'crossword/index.html', {
                    'form': form,
                    'draw_form': DrawForm(),
                    'show_demo': id,
                })
            else:
                response = render(request, 'crossword/index.html', {
                    'form': form,
                    'show_demo': 0,
                })
            response.set_cookie(key='name', value=name)
            response.set_cookie(key='describe', value=crossword.describe)
            response.set_cookie(key='arr', value=crossword.best_crossword)
            response.set_cookie(key='text', value=text)
            return response
        else:
            response = render(request, 'crossword/index.html', {
                'form': form,
            })
            return response
        
def draw(request):
    if request.GET:
        form = DrawForm(request.GET)
        gen_form = NewCrosswordForm(initial={'words': request.COOKIES.get('text'), 'name': request.COOKIES.get('name')})
        if form.is_valid():
            quality = int(request.GET['quality'])
            id = request.COOKIES.get('id')
            best_crossword = ast.literal_eval(request.COOKIES.get('arr'))
            description = ast.literal_eval(request.COOKIES.get('describe'))
            name = request.COOKIES.get('name')
            
            crossword = Crossword()
            crossword.name = name
            crossword.describe = description
            crossword.best_crossword = best_crossword
            crossword.draw(zoom_parameter=quality, id=id)

            return render(request, 'crossword/index.html', {
                'form': gen_form,
                'draw_form': DrawForm(),
                'download': request.COOKIES.get('id'),
                'crossword_name': name,
            })
        else:
            return render(request, 'crossword/index.html', context={
                'form': gen_form,
                'draw_form': DrawForm(),
            })