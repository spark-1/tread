from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_protect
from .collector.naverDataLab import NaverDataLab
from datetime import datetime
import json
# Create your views here.
def home_page(request):
    return render(request, 'treadweb/base.html')

@cache_page(60 * 15)
@csrf_protect
def search_page(request):
    naver = NaverDataLab()
    now = datetime.now()
    time = now.strftime("%Y-%m-%dT%H:%M:%S")
    keyword_rank = naver.naver_searchlist(time)
    if request.method == "POST" and request.POST.get("keyword"):
        return search_keyword(request, request.POST.get("keyword"))
    return render(request, 'treadweb/base_search.html', {"keyword_rank": keyword_rank})

@cache_page(60 * 15)
@csrf_protect
def search_keyword(request, keyword):
    naver = NaverDataLab()
    now = datetime.now()
    time = now.strftime("%Y-%m-%dT%H:%M:%S")
    keyword_rank = naver.naver_searchlist(time)
    line_result = [
            ["data1", 30, 200, 100, 400, 150, 250],
            ["data2", 50, 20, 10, 40, 15, 25]
    ]
    bar_result = [
        ["data1", 30, 200, 100, 400, 150, 250],
        ["data2", 50, 20, 10, 40, 15, 25]
    ]
    donut_result = [
        ["data1", 30],
        ["data2", 50]
    ]
    return render(request, 'treadweb/base_search.html', {
        'keyword_rank': keyword_rank,
        'line_result': json.dumps(line_result),
        'bar_result': json.dumps(bar_result),
        'donut_result': json.dumps(donut_result)
    })

def rank_page(request):
    return render(request, 'treadweb/base_rank.html')

def movie_page(request):
    return render(request, 'treadweb/base_movie.html')
