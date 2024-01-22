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
            text = str(form.cleaned_data.get('words'))
            name = form.cleaned_data.get('name')
            gen_form = NewCrosswordForm(initial={'words': text, 'name': name})
            response = render(request, 'crossword/index.html', {
                'form': gen_form,
            })
        else:
            response = render(request, 'crossword/index.html', {
                'form': NewCrosswordForm(),
            })
    else:
        if request.COOKIES.get('id') == None:
            messages.success(request, 'Вітаємо на форумі. Для початку пропонуємо вам ознайомитись зі сторінкою "Про проєкт".')
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
            name = str(form.cleaned_data['name'])
            text = form.cleaned_data['words']
            time = form.cleaned_data['time']
            
            id = request.COOKIES.get('id')
            try:
                crossword.read(text)
                crossword.name = name
            except:
                messages.error(request, 'Нажаль не вдалося зчитати текст, який ви написали. Радимо притримуватися правил запису слів, які вказані на сторінці "Про проєкт".')
                response = render(request, 'crossword/index.html', {
                    'form': form,
                })
                return response

            try:
                crossword.generate(int(time))
            except:
                messages.error(request,
                               'Нажаль не вдалося згенерувати кросворд. У такому разі просимо зв\'язатися з власником, контакти якого зазначено на сторінці "Про проєкт", та повідомити про помилку.')
                response = render(request, 'crossword/index.html', {
                    'form': form,
                })
                return response

            if crossword.best_crossword != []:
                try:
                    crossword.draw('full_demo', 15, id)
                except:
                    messages.error(request, 'Нажаль не вдалося намалювати кросворд. Радимо прибрати специфічні символи зі слів та опису до них.')
                    response = render(request, 'crossword/index.html', {
                        'form': form,
                    })
                    return response

                draw_form = DrawForm(initial={'words': text, 'name': name, 'best_crossword': str(crossword.best_crossword)})
                posting_form = PostingForm(initial={'words': text, 'name': name, 'best_crossword': str(crossword.best_crossword)})
                
                response = render(request, 'crossword/index.html', {
                    'form': form,
                    'draw_form': draw_form,
                    'show_demo': id,
                    'posting_form': posting_form,
                })
            else:
                messages.error(request, "На жаль, ми не змогли створити кросворд за вашими словами. Радимо додати більше слів та прибрати маленькі слова.")
                response = render(request, 'crossword/index.html', {
                    'form': form,
                })

            #response.set_cookie(key='name', value=name.encode('utf-8'))
            #response.set_cookie(key='crossword', value=str(crossword.best_crossword).encode('utf-8'))
            #response.set_cookie(key='text', value=text.encode('utf-8'))
            return response
        else:
            response = render(request, 'crossword/index.html', {
                'form': form,
            })
            return response
        
def draw(request, link):
    if request.method == 'POST':
        form = DrawForm(request.POST)
        if form.is_valid():
            quality = int(form.cleaned_data['quality'])
            best_crossword = ast.literal_eval(form.cleaned_data['best_crossword'])
            text = str(form.cleaned_data['words'])
            name = str(form.cleaned_data['name'])

            id = request.COOKIES.get('id')


            if link == 'index':
                path = 'crossword/index.html'
                gen_form = NewCrosswordForm(
                    initial={'words': text, 'name': name})
            else:
                path = 'crossword/demo.html'
                gen_form = DemoCrosswordForm(
                    initial={'words': text, 'name': name})

            user_status = '0'

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
            
            if user_status == '0':
                crossword.draw('full', zoom_parameter=quality, id=id)
            else:
                crossword.draw('clear', zoom_parameter=quality, id=id)

            draw_form = DrawForm(initial={'words': text, 'name': name, 'best_crossword': best_crossword, 'quality': quality})
            posting_form = PostingForm(initial={'words': text, 'name': name, 'best_crossword': str(crossword.best_crossword)})

            return render(request, path, {
                'form': gen_form,
                'draw_form': draw_form,
                'download': id,
                'crossword_name': name,
                'show_demo': id,
                'posting_form': posting_form,
                'user_status': user_status,
            })
        else:
            return render(request, 'crossword/index.html', {
                'form': NewCrosswordForm(),
            })
        
def post_crossword(request):
    if request.method == 'POST':
        form = PostingForm(request.POST)
        if form.is_valid():
            status = form.cleaned_data['status']
            language = form.cleaned_data['language']
            best_crossword = ast.literal_eval(form.cleaned_data['best_crossword'])
            text = str(form.cleaned_data['words'])
            name = str(form.cleaned_data['name'])

            id = request.COOKIES.get('id')

            link = name.replace(' ', '_')

            all_links = CW_db.objects.values_list('link', flat=True)
            draw_form = DrawForm(initial={'words': text, 'name': name, 'best_crossword': best_crossword})
            if link in all_links:
                gen_form = NewCrosswordForm(initial={'words': text, 'name': name})
                messages.error(request, "Неприпустиме значення назви. Для того, щоб опублікувати, назва повинна мати незайняте значення.")
                return render(request, 'crossword/index.html', {
                    'form': gen_form,
                    'draw_form': draw_form,
                    'show_demo': id,
                })
            if not(bool(re.search('^[a-zA-Zа-яА-Я0-9_ґҐіІЇїєЄ\'-]*$', link))):
                gen_form = NewCrosswordForm(initial={'words': text, 'name': name})
                messages.error(request, "Неприпустиме значення назви. Для того, щоб опублікувати, назва повинна містити лише допустимі символи (латиниця, кирилиця, тире, нижнє підкреслення, пробіл).")
                return render(request, 'crossword/index.html', {
                    'form': gen_form,
                    'draw_form': draw_form,
                    'show_demo': id,
                })
            if len(name) > 64:
                gen_form = NewCrosswordForm(initial={'words': text, 'name': name})
                messages.error(request, "Неприпустиме значення назви. Для того, щоб опублікувати, назва повинна містити не більше 64 символів.")
                return render(request, 'crossword/index.html', {
                    'form': gen_form,
                    'draw_form': draw_form,
                    'show_demo': id,
                })
            if len(best_crossword) > 131072 or len(text) > 131072:
                gen_form = NewCrosswordForm(initial={'words': text, 'name': name})
                messages.error(request, "Неприпустимий опис. Для того, щоб опублікувати, зменшіть кількість слів або опис до них.")
                return render(request, 'crossword/index.html', {
                    'form': gen_form,
                    'draw_form': draw_form,
                    'show_demo': id,
                })
            
            new_crossword = CW_db.objects.create(name=name,
                                                    crossword=best_crossword,
                                                    describe=text,
                                                    link=link,
                                                    creator_id=int(User_db.objects.values('pk').get(user_name=request.user.username)['pk']),
                                                    status=status,
                                                    language=language)
            new_crossword.save()

            messages.success(request, 'Кросворд вдало опублікований!')

            return HttpResponseRedirect(reverse('main:show_crossword', args=(link, )))

    
def delete_crossword(request, crossword_link):
    crossword_info = CW_db.objects.get(link=crossword_link)
    crossword_name = crossword_info.name
    creator_id = crossword_info.creator_id
    creator_name = User_db.objects.values('user_name').get(pk=creator_id)['user_name']
    if creator_name == request.user.username:
        messages.success(request, f"Кросворд '{crossword_name}' вдало видалено!")
        CW_db.objects.filter(link=crossword_link).delete()
    else:
        messages.error(request, f"Ви не маєте право видаляти цей кросворд.")
    return HttpResponseRedirect(reverse('main:index'))


def show_crossword(request, link):
    check_db = CW_db.objects.filter(link=link)
    if len(check_db) != 1:
        messages.error(request, 'Не існує кросворда за вказаним посиланням.')
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

    demo_form = DemoCrosswordForm(initial={'words': '', 'name': ''})

    crossword = Crossword()
    crossword.read(text)
    crossword.name = name
    crossword.best_crossword = ast.literal_eval(best_crossword)
    if user_status == '0':
        crossword.draw('full_demo', 15, id)
        demo_form = DemoCrosswordForm(initial={'words': text, 'name': name})
    elif user_status == '1':
        crossword.draw('clear_demo', 15, id)


    if user_status == '2':
        messages.info(request, f"Ви не маєте право бачити приватні кросворди інших користувачів.")
        return HttpResponseRedirect(reverse('main:ask_search', args=('page=0', )))
        return response


    draw_form = DrawForm(initial={'words': text, 'name': name, 'best_crossword': str(crossword.best_crossword)})
    
    response = render(request, 'crossword/demo.html', {
        'form': demo_form,
        'draw_form': draw_form,
        'show_demo': id,
        'crossword_name': name,
        'crossword_link': link,
        'user_status': user_status,
        'is_owner': is_owner,
    })

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
            if not(bool(re.search('^[a-zA-Zа-яА-Я0-9-_ ]*$', data['ask']))) or not(bool(re.search('^[a-zA-Z0-9_.+@-]*$', data['creator']))):
                messages.error(request, "Неприпустиме значення назви або креатора для пошуку.")
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

    if question != '':
        answer_db_info = answer_db_info.filter(name__contains=question)
    if creator != '':
        if User_db.objects.filter(user_name=creator).count() == 1:
            answer_db_info = answer_db_info.filter(creator_id=User_db.objects.values('pk').get(user_name=creator)['pk'])
        else:
            messages.success(request, 'Не існує користувача за вказаним user_name.')
            answer_db_info = answer_db_info.filter(pk=0)
    if language != '' and language != '$$':
        answer_db_info = answer_db_info.filter(language__contains=language)
    if status != '' and status != '$$':
        answer_db_info = answer_db_info.filter(status__contains=status)
    if status == '2':
        answer_db_info = answer_db_info.filter(creator_id=User_db.objects.values('pk').get(user_name=request.user.username)['pk'])

    answer_db_info = answer_db_info.reverse()
    answer_db_info = answer_db_info.values('name', 'link', 'creator_id', 'language', 'status')
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
            
            messages.success(request, f'Вітаю! Акаунт {username} вдало створено. Можете війти під цим обліковим записом.')
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
        messages.error(request, 'Не існує користувача за вказаним посиланням.')
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

def no_page(request, link):
    messages.error(request, "Не існує сторінки за вказаним посиланням.")
    return HttpResponseRedirect(reverse('main:index'))

def test_button(request):
    user_id = request.COOKIES.get('id')
    print(user_id)
    print('End!!!!!!')
    return render(request, 'crossword/test.html')