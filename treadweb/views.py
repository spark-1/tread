from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_protect
from .collector.naverDataLab import NaverDataLab
from .collector.googleTrend import GoogleTrend
from datetime import datetime
from .collector.youtube_api_channelInfo import ChannelInfo
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
    line_result = naver.keyword_search(keyword)
    keywords = []
    keywords.append(keyword)
    googletrend = GoogleTrend(keyword=keywords)
    googletrend.set_payload()
    googletrend.interest_by_region()
    region_result = googletrend.interest_by_region_df_to_list()
    # region_result = [
    #     ["data1", 30, 200, 100, 400, 150, 250],
    #     ["data2", 50, 20, 10, 40, 15, 25]
    # ]
    donut_result = [
        ["male", 30],
        ["female", 50]
    ]
    return render(request, 'treadweb/base_search.html', {
        'keyword_rank': keyword_rank,
        'line_result': json.dumps(line_result),
        'region_result': json.dumps(region_result),
        'donut_result': json.dumps(donut_result)
    })

def channel_page(request):

    return render(request, 'treadweb/base_channel.html',
                  {'tag_list': ChannelInfo.channel_tags}
                  )

def video_page(request):
    return render(request, 'treadweb/base_video.html')
