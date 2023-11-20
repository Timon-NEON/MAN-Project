from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


import random
import ast
import re
import time

from .forms import *
from .constants import *
from crossword.main_algorithm.CW import Crossword
from .models import Crosswords as CW_db
from .models import Users as User_db

    
def index(request):
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
        if request.COOKIES.get('id') == None:
            messages.success(request, 'My greating! Let\'s read page About')
        response = render(request, 'crossword/index.html', {
            'form': NewCrosswordForm(),
        })
    if request.COOKIES.get('id') == None:
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
                crossword.draw('full_demo', 15, id)
                
                response = render(request, 'crossword/index.html', {
                    'form': form,
                    'draw_form': DrawForm(),
                    'show_demo': id,
                    'posting_form': PostingForm(),
                })
            else:
                response = render(request, 'crossword/index.html', {
                    'form': form,
                    'show_demo': 0,
                })

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
            user_status = 0

            if link == 'demo':
                db_info = CW_db.objects.get(link=name.replace(' ', '_'))
                user_status = db_info.status
                creator_id = db_info.creator_id
                if user_status != '0':
                    if User_db.objects.values('user_name').get(pk=creator_id)['user_name'] == request.user.username:
                        user_status = '0'
            
            crossword = Crossword()
            crossword.name = name
            crossword.best_crossword = best_crossword

            crossword.read(text)
            
            if user_status == 0:
                crossword.draw('full', zoom_parameter=quality, id=id)
            else:
                crossword.draw('clear', zoom_parameter=quality, id=id)

            return render(request, path, {
                'form': gen_form,
                'draw_form': DrawForm(),
                'download': request.COOKIES.get('id'),
                'crossword_name': name,
                'show_demo': id,
                'posting_form': PostingForm(),
                'user_status': user_status,
            })
        else:
            return render(request, path, context={
                'form': gen_form,
                'draw_form': DrawForm(),
                'show_demo': id,
                'posting_form': PostingForm(),
                'user_status': user_status,
            })
        
def post_crossword(request):
    if request.GET:
        form = PostingForm(request.GET)
        if form.is_valid():
            status = request.GET['status']
            language = request.GET['language']
            link = request.COOKIES.get('name').replace(' ', '_')
            id = request.COOKIES.get('id')

            all_links = CW_db.objects.values_list('link', flat=True)
            if link in all_links:
                gen_form = NewCrosswordForm(initial={'words': request.COOKIES.get('text'), 'name': request.COOKIES.get('name')})
                messages.error(request, "Неприпустиме значення назви. Для того, щоб запостити, назва повинна мати незайняте значення.")
                return render(request, 'crossword/index.html', {
                    'form': gen_form,
                    'draw_form': DrawForm(),
                    'show_demo': id,
                })
            if not(bool(re.search('^[a-zA-Z0-9_-]*$', link))):
                gen_form = NewCrosswordForm(initial={'words': request.COOKIES.get('text'), 'name': request.COOKIES.get('name')})
                messages.error(request, "Неприпустиме значення назви. Для того, щоб запостити назва повинна містити лише допустимі символи (a-z, A-Z, _, -, space).")
                return render(request, 'crossword/index.html', {
                    'form': gen_form,
                    'draw_form': DrawForm(),
                    'show_demo': id,
                })
            if len(request.COOKIES.get('name')) > 64:
                gen_form = NewCrosswordForm(initial={'words': request.COOKIES.get('text'), 'name': request.COOKIES.get('name')})
                messages.error(request, "Неприпустиме значення назви. Для того, щоб запостити назва повинна містити не більше 64 символів.")
                return render(request, 'crossword/index.html', {
                    'form': gen_form,
                    'draw_form': DrawForm(),
                    'show_demo': id,
                })
            if len(request.COOKIES.get('crossword')) > 131072 or len(request.COOKIES.get('text')) > 131072:
                gen_form = NewCrosswordForm(initial={'words': request.COOKIES.get('text'), 'name': request.COOKIES.get('name')})
                messages.error(request, "Неприпустимий опис. Для того, щоб запостити, зменшіть кількість слів або опис до них.")
                return render(request, 'crossword/index.html', {
                    'form': gen_form,
                    'draw_form': DrawForm(),
                    'show_demo': id,
                })
            
            new_crossword = CW_db.objects.create(name=request.COOKIES.get('name'),
                                                    crossword=request.COOKIES.get('crossword'),
                                                    describe=request.COOKIES.get('text'),
                                                    link=link,
                                                    creator_id=int(User_db.objects.values('pk').get(user_name=request.user.username)['pk']),
                                                    status=status,
                                                    language=language)
            new_crossword.save()

            messages.success(request, 'Crossword successfully added')

            return HttpResponseRedirect(reverse('main:show_crossword', args=(link, )))

    
def delete_crossword(request, crossword_link):
    crossword_info = CW_db.objects.get(link=crossword_link)
    crossword_name = crossword_info.name
    creator_id = crossword_info.creator_id
    creator_name = User_db.objects.values('user_name').get(pk=creator_id)['user_name']
    if creator_name == request.user.username:
        messages.success(request, f"Crossword '{crossword_name}' successfully deleted")
        CW_db.objects.filter(link=crossword_link).delete()
    else:
        messages.success(request, f"You can't delete crossword becouse you are not creator")
    return HttpResponseRedirect(reverse('main:index'))


def show_crossword(request, link):
    check_db = CW_db.objects.filter(link=link)
    if len(check_db) != 1:
        messages.success(request, 'Here is no crossword with this link')
        return render(request, 'crossword/index.html', {
            'form': NewCrosswordForm(),
        })
    db_info = check_db[0]
    name = db_info.name
    best_crossword = db_info.crossword
    text = db_info.describe
    creator_id = db_info.creator_id
    user_status = db_info.status
    id = request.COOKIES.get('id')
    is_owner = False
    
    creator_name = User_db.objects.values('user_name').get(pk=creator_id)['user_name']
    
    if creator_name == request.user.username:
        user_status = '0'
        is_owner = True

    demo_form = DemoCrosswordForm(initial={'words': request.COOKIES.get('text'), 'name': name})

    crossword = Crossword()
    crossword.read(text)
    crossword.name = name
    crossword.best_crossword = ast.literal_eval(best_crossword)
    if user_status == '0':
        crossword.draw('full_demo', 15, id)
    elif user_status == '1':
        crossword.draw('clear_demo', 15, id)

    if user_status == '2':
        messages.success(request, f"You can't see that crossword, becouse you are nor creator")
        return HttpResponseRedirect(reverse('main:ask_search', args=('page=0', )))
        return response
    
    
    response = render(request, 'crossword/demo.html', {
        'form': demo_form,
        'draw_form': DrawForm(),
        'show_demo': id,
        'crossword_name': name,
        'crossword_link': link,
        'user_status': user_status,
        'is_owner': is_owner,
    })
        
    response.set_cookie(key='name', value=name)
    response.set_cookie(key='crossword', value=best_crossword)
    response.set_cookie(key='text', value=text)

    return response

def get_link_info(link):
    data = link.split('~~')
    ask = {}
    for pair in data:
        info = pair.split('=')
        ask[info[0]] = info[1]
    for value in link_template:
        if value not in ask:
            ask[value] = ''
    return ask

def create_link(data):
    link = ''
    for value in link_template:
        if str(data[value]) != '':
            link += value + '=' + str(data[value]) + '~~'
    return link[:-2]


def search_forward(request, ask):
    data_link = get_link_info(ask)
    data_link['page'] = int(data_link['page']) + 1
    link = create_link(data_link)
    return HttpResponseRedirect(reverse('main:ask_search', args=(link, )))

def search_backward(request, ask):
    data_link = get_link_info(ask)
    data_link['page'] = int(data_link['page']) - 1
    link = create_link(data_link)
    return HttpResponseRedirect(reverse('main:ask_search', args=(link, )))

def search_extract_data(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            data = {}
            data['ask'] = form.cleaned_data['ask']
            data['creator'] = form.cleaned_data['creator']
            data['language'] = form.cleaned_data['language']
            data['status'] = form.cleaned_data['status']
            data['page'] = 0
            if not(bool(re.search('^[a-zA-Z0-9-_ ]*$', data['ask']))) or not(bool(re.search('^[a-zA-Z0-9_-]*$', data['creator']))):
                messages.error(request, "Неприпустиме значення назви or creator.")
                return HttpResponseRedirect(reverse('main:ask_search', args=('page=0', )))
            link = create_link(data)
            return HttpResponseRedirect(reverse('main:ask_search', args=(link, )))

def search(request, ask):

    data_link = get_link_info(ask)
    question = data_link['ask']
    page = int (data_link['page'])
    creator = data_link['creator']
    language = data_link['language']
    status = data_link['status']

    search_form = SearchForm(initial={'ask': question, 'creator': creator, 'language':language, 'status': status})
    
    answer_db_info = CW_db.objects.all().order_by('pk')
    print(answer_db_info)

    if question != '':
        answer_db_info = answer_db_info.filter(name__contains=question)
    if creator != '':
        if User_db.objects.filter(user_name=creator).count() == 1:
            print(answer_db_info)
            print(question)
            answer_db_info = answer_db_info.filter(creator_id=User_db.objects.values('pk').get(user_name=creator)['pk'])
            print(answer_db_info)
        else:
            messages.success(request, 'User not found')
            answer_db_info = answer_db_info.filter(pk=0)
    if language != '' and language != '##':
        answer_db_info = answer_db_info.filter(language__contains=language)
    if status != '' and status != '##':
        answer_db_info = answer_db_info.filter(status__contains=status)
    if status == '2':
        answer_db_info = answer_db_info.filter(creator_id=User_db.objects.values('pk').get(user_name=request.user.username)['pk'])

    answer_db_info = answer_db_info.reverse()
    answer_db_info = answer_db_info.values('name', 'link', 'creator_id')
    if (len(answer_db_info)) != 0:
        max_page = (len(answer_db_info) - 1) // max_search_rows
    else:
        max_page = 0

    if page == max_page:
        send_info = answer_db_info[page * max_search_rows:]
    else:
        send_info = answer_db_info[page * max_search_rows: (page + 1) * max_search_rows]

    for crossword_element in send_info:
        creator_info = User_db.objects.get(pk=crossword_element['creator_id'])
        crossword_element['creator_name'] = creator_info.user_name

    #if search_form == None:
    #    search_form = SearchForm()
    return render(request, 'crossword/search.html', {
        'name_link': send_info,
        'max_page': max_page,
        'link': ask,
        'page': page,
        'start_value': max_search_rows * page + 1,
        'search_form': search_form,
    })

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('first_name')
            second_name = form.cleaned_data.get('second_name')
            email = form.cleaned_data.get('email')
            
            messages.success(request, f'Hi, {username}, your account was created successfully!')
            new_user = User_db.objects.create(user_name = username,
                                              first_name = first_name,
                                              second_name = second_name,
                                              email = email,
                                              sign_up_time = time.strftime("%d.%m.%G", time.gmtime(time.time())))
            new_user.save()
            return redirect('main:index')
        return render(request, 'crossword/registration.html', {
            'form': form,
        })
    form = UserRegisterForm()
    return render(request, 'crossword/registration.html', {
        'form': form,
    })


    
def user_page(request, username):
    check_db = User_db.objects.filter(user_name=username)
    if len(check_db) != 1:
        messages.success(request, 'Here is no user with this user_name')
        return render(request, 'crossword/index.html', {
            'form': NewCrosswordForm(),
        })
    user_data = check_db[0]
    return render(request, 'crossword/user_page.html', {
        'username': username,
        'user_data': user_data,
    })

def about_page(request):
    return render(request, 'crossword/about_page.html')

def test_button(request):
    user_id = request.COOKIES.get('id')
    print(user_id)
    print('End!!!!!!')
    return render(request, 'crossword/index.html')