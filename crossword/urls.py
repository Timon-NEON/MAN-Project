from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_view

from . import views

app_name = 'main'
urlpatterns = [
    path('', views.index, name='index'),
    path('generate', views.generate, name='generate'),
    path('draw/<str:link>', views.draw, name='draw'),
    path('post', views.post_crossword, name='post'),

    #path('test/', views.test_button, name='test'),
    path('about/', views.about_page, name='about'),

    path('crossword/<str:link>', views.show_crossword, name='show_crossword'),
    path('delete/<str:crossword_link>', views.delete_crossword, name='delete'),

    path('search_forward/<str:ask>', views.search_forward, name='forward_search'),
    path('search_backward/<str:ask>', views.search_backward, name='backward_search'),
    path('search_extract_data', views.search_extract_data, name='search_extract_data'),
    path('search/<str:ask>', views.search, name='ask_search'),
    path('user/<str:username>', views.user_page, name='user_page'),
    
    path('register/', views.register, name='register'),
    path('login/', auth_view.LoginView.as_view(template_name='crossword/login.html'), name="login"),
    path('logout/', auth_view.LogoutView.as_view(), name='logout'),

    path('<str:link>', views.no_page, name='no_page'),
]
