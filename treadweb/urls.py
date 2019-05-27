from django.urls import path
from django.urls import re_path
from . import views

app_name = 'treadweb'
urlpatterns = [
    re_path(r'^$', views.home_page, name='home'),
    re_path(r'^search/$', views.search_page, name='search'),
    path('search/<str:keyword>', views.search_keyword, name='search_keyword'),
    path('rank/', views.rank_page, name='rank'),
    path('movie/', views.movie_page, name='movie'),
]
