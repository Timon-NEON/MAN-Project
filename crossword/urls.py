from django.contrib import admin
from django.urls import path, include

from . import views

app_name = 'main'
urlpatterns = [
    path('', views.index, name='index'),
    path('generate', views.generate, name='generate'),
    path('draw/<str:link>', views.draw, name='draw'),
    path('post', views.post_crossword, name='post'),
    path('crossword/<str:link>', views.show_crossword, name='show_crossword'),
    path('search_forward/<str:ask>', views.search_forward, name='forward_search'),
    path('search_backward/<str:ask>', views.search_backward, name='backward_search'),
    path('search/<str:ask>', views.search, name='ask_search'),
    path('', include('django.contrib.auth.urls')),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('user/<str:username>', views.user_page, name='user_page')
]
