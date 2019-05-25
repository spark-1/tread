from django.shortcuts import render
from django.views import generic
from .collector.naver import naverData
from datetime import datetime

# Create your views here.
def home_page(request):
    now = datetime.now()
    keywords = naverData.naver_searchlist(now.year, now.month, now.day, now.hour, now.minute, now.second)
    return render(request, 'treadweb/base.html', {'keywords': keywords})

def search_page(request):
    return render(request, 'treadweb/base_search.html')

def rank_page(request):
    return render(request, 'treadweb/base_rank.html')

def movie_page(request):
    return render(request, 'treadweb/base_movie.html')
