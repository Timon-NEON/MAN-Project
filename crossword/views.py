from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django import forms


import random
import copy
import ast
import re

from .forms import *
from crossword.main_algorithm.CW import Crossword
from .models import Crosswords as CW_db

# Create your views here.



class DrawForm(forms.Form):
    CHOICES = (
    (5, 'Low'),
    (10, 'Medium'),
    (20, 'Big')
    )
    quality = forms.ChoiceField(choices=CHOICES)

    
def index(request):
    #if 'ses_info' not in request.session:
    #    request.session['ses_info'] = {'id':random.randint(1, 100000), 'form': None}
    if request.method == 'POST':
        form = DemoCrosswordForm(request.POST)
        if form.is_valid():
            gen_form = NewCrosswordForm(initial={'words': request.COOKIES.get('text'), 'name': request.COOKIES.get('name')})
            response = render(request, 'crossword/index.html', {
                'form': gen_form,
            })
        else:
            response = render(request, 'crossword/index.html', {
                'form': NewCrosswordForm(),
            })
    else:
        response = render(request, 'crossword/index.html', {
            'form': NewCrosswordForm(),
        })
    response.set_cookie(key='id', value=str(random.randint(1, 100000)))
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
            print(name)
            print(crossword.best_crossword)
            print(text)
            response.set_cookie(key='name', value=name)
            response.set_cookie(key='crossword', value=crossword.best_crossword)
            response.set_cookie(key='text', value=text)
            return response
        else:
            response = render(request, 'crossword/index.html', {
                'form': form,
            })
            return response
        
def draw(request, link):
    if link == 'index':
        path = 'crossword/index.html'
        gen_form = NewCrosswordForm(initial={'words': request.COOKIES.get('text'), 'name': request.COOKIES.get('name')})
    else:
        path = 'crossword/demo.html'
        gen_form = DemoCrosswordForm(initial={'words': request.COOKIES.get('text'), 'name': request.COOKIES.get('name')})
    if request.GET:
        form = DrawForm(request.GET)
        if form.is_valid():
            quality = int(request.GET['quality'])
            id = request.COOKIES.get('id')
            best_crossword = ast.literal_eval(request.COOKIES.get('crossword'))
            text = request.COOKIES.get('text')
            name = request.COOKIES.get('name')
            
            crossword = Crossword()
            crossword.name = name
            crossword.best_crossword = best_crossword

            crossword.read(text)

            crossword.draw(zoom_parameter=quality, id=id)

            return render(request, path, {
                'form': gen_form,
                'draw_form': DrawForm(),
                'download': request.COOKIES.get('id'),
                'crossword_name': name,
                'show_demo': id,
            })
        else:
            return render(request, path, context={
                'form': gen_form,
                'draw_form': DrawForm(),
                'show_demo': id,
            })
        
def post_crossword(request):
    if request.method == 'POST':
        link = request.COOKIES.get('name').replace(' ', '_')
        id = request.COOKIES.get('id')

        all_links = CW_db.objects.values_list('link', flat=True)
        if link in all_links:
            gen_form = NewCrosswordForm(initial={'words': request.COOKIES.get('text'), 'name': request.COOKIES.get('name')})
            return render(request, 'crossword/index.html', {
                'form': gen_form,
                'draw_form': DrawForm(),
                'show_demo': id,
                'error': "Неприпустиме значення назви. Для того, щоб запостити, назва повинна мати незайняте значення."
            })
        if not(bool(re.search('^[a-zA-Z0-9-_]*$', link))):
            gen_form = NewCrosswordForm(initial={'words': request.COOKIES.get('text'), 'name': request.COOKIES.get('name')})
            return render(request, 'crossword/index.html', {
                'form': gen_form,
                'draw_form': DrawForm(),
                'show_demo': id,
                'error': "Неприпустиме значення назви. Для того, щоб запостити назва повинна містити лише допустимі символи (a-z, A-Z, _, space)."
            })
        if len(request.COOKIES.get('name')) > 64:
            gen_form = NewCrosswordForm(initial={'words': request.COOKIES.get('text'), 'name': request.COOKIES.get('name')})
            return render(request, 'crossword/index.html', {
                'form': gen_form,
                'draw_form': DrawForm(),
                'show_demo': id,
                'error': "Неприпустиме значення назви. Для того, щоб запостити назва повинна містити не більше 64 символів."
            })
        if len(request.COOKIES.get('crossword')) > 131072 or len(request.COOKIES.get('text')) > 131072:
            gen_form = NewCrosswordForm(initial={'words': request.COOKIES.get('text'), 'name': request.COOKIES.get('name')})
            return render(request, 'crossword/index.html', {
                'form': gen_form,
                'draw_form': DrawForm(),
                'show_demo': id,
                'error': "Неприпустимий опис. Для того, щоб запостити, зменшіть кількість слів або опис до них."
            })
        new_crossword = CW_db.objects.create(name=request.COOKIES.get('name'),
                                                crossword=request.COOKIES.get('crossword'),
                                                describe=request.COOKIES.get('text'),
                                                link=link)
        return HttpResponseRedirect(reverse('main:show_crossword', args=(link, )))

    
def show_crossword(request, link):
    db_info = CW_db.objects.get(link=link)
    name = db_info.name
    best_crossword = db_info.crossword
    text = db_info.describe
    likes = db_info.likes
    id = request.COOKIES.get('id')

    demo_form = DemoCrosswordForm(initial={'words': request.COOKIES.get('text'), 'name': request.COOKIES.get('name')})

    crossword = Crossword()
    crossword.read(text)
    crossword.name = name
    crossword.best_crossword = ast.literal_eval(best_crossword)
    crossword.draw(15, id, True)
    
    response = render(request, 'crossword/demo.html', {
        'form': demo_form,
        'draw_form': DrawForm(),
        'show_demo': id,
        'name': name,
    })
    response.set_cookie(key='name', value=name)
    response.set_cookie(key='crossword', value=best_crossword)
    response.set_cookie(key='text', value=text)

    return response

def search_forward(request, ask):
    data = ask.split('~~')
    page = int(data[1].split('=')[1]) + 1
    link = data[0] + '~~page=' + str(page)
    return HttpResponseRedirect(reverse('main:ask_search', args=(link, )))

def search_backward(request, ask):
    data = ask.split('~~')
    page = int(data[1].split('=')[1]) - 1
    link = data[0] + '~~page=' + str(page)
    return HttpResponseRedirect(reverse('main:ask_search', args=(link, )))

def search(request, ask):
    #ask=val~~page=1
    max_rows = 10
    
    data = ask.split('~~')
    question = data[0].split('=')[1]
    page = int(data[1].split('=')[1])
    
    name_link = CW_db.objects.values('name', 'link').all()

    if (len(name_link)) != 0:
        max_page = (len(name_link) - 1) // max_rows
    else:
        max_page = 0

    if page == max_page:
        send_info = name_link[page * max_rows:]
    else:
        send_info = name_link[page * max_rows: (page + 1) * max_rows]

    #page * max_rows: (page + 1) * max_rows

    print('name_link: ', name_link)

    for info in send_info:
        print(info['name'], info['link'])

    

    return render(request, 'crossword/search.html', {
        'name_link': send_info,
        'max_page': max_page,
        'link': ask,
        'page': page,
        'start_value': max_rows * page + 1,
    })
    
def user_page(request):
    pass
    #