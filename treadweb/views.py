from django.shortcuts import render
from django.views import generic
from .collector.naver import naverData
from datetime import datetime
import json

# Create your views here.
def home_page(request):
    return render(request, 'treadweb/base.html')

def search_page(request):
    return render(request, 'treadweb/base_search.html')

def search_keyword(request, keyword):
    line_result = [
            ["data1", 30, 200, 100, 400, 150, 250],
            ["data2", 50, 20, 10, 40, 15, 25]
    ]
    return render(request, 'treadweb/base_search.html', {'line_result': json.dumps(line_result)})

def rank_page(request):
    return render(request, 'treadweb/base_rank.html')

def movie_page(request):
    return render(request, 'treadweb/base_movie.html')
