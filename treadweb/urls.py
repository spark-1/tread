from django.urls import path
from django.urls import re_path
from . import views

app_name = 'treadweb'
urlpatterns = [
    path('', views.home_page, name='home'),
    path('search/', views.search_page, name='search'),
    path('rank/', views.rank_page, name='rank'),
    path('movie/', views.movie_page, name='movie'),
]
