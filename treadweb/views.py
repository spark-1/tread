from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_protect
from treadweb.collector.naverDataLab import NaverDataLab
from treadweb.collector.googleTrend import GoogleTrend
from datetime import datetime
from treadweb.collector.youtube_api_channelInfo import ChannelInfo
from treadweb.collector.youtube_api_search import YoutubeSearch
from multiprocessing import Process
import os

import json
# Create your views here.
def home_page(request):
    return render(request, 'treadweb/base_home.html')

@cache_page(10)
@csrf_protect
def search_page(request):
    naver = NaverDataLab()
    now = datetime.now()
    time = now.strftime("%Y-%m-%dT%H:%M:%S")
    keyword_rank = naver.naver_searchlist(time)
    return render(request, 'treadweb/base_search.html', {"keyword_rank": keyword_rank})

@cache_page(10)
@csrf_protect
def search_keyword(request, keyword):
    naver = NaverDataLab()
    pr1 = Process(target=naver.draw_cloud, args=(keyword,))
    pr1.start()
    line_result = naver.load_data(keyword)
    keywords = list()
    keywords.append(keyword)
    googletrend = GoogleTrend(keyword=keywords)
    googletrend.set_payload()
    region_result = googletrend.load_data('region')
    donut_result = googletrend.load_data('gender')
    pr1.join()
    WC_exists = 'yes' if os.path.exists('treadweb/static/treadweb/img/wordcloud.png') else 'no'
    return JsonResponse({
        'line_result': line_result,
        'region_result': region_result,
        'gender_result': donut_result,
        'WC_exists': WC_exists
    }, json_dumps_params={'ensure_ascii': True})

def channel_page(request):
    youtube = YoutubeSearch()
    channels = youtube.search_channel_orderby_view();
    channel_list = []
    channel_info = ChannelInfo()
    for channel in channels:
        channel_data = channel_info.get_channel_data(channel["channel_id"])
        channel_list.append(channel_data)

    return render(request, 'treadweb/base_channel.html',
                  {
                      'channel_list': channel_list
                    }
                  )

def video_page(request):
    youtube = YoutubeSearch()
    tag_keys = list(youtube.tags.keys())
    n = len(tag_keys) // 2
    tag_list = [tag_keys[:n], tag_keys[n + 1:]]
    video_list = youtube.search_video_by_category(0)
    return render(request, 'treadweb/base_video.html',
                  {
                      'tag_list': tag_list,
                      'video_list': video_list
                    }
                  )


def video_tag(request, tag):
    youtube = YoutubeSearch()
    tag_keys = list(youtube.tags.keys())
    n = len(tag_keys) // 2
    tag_list = [tag_keys[:n], tag_keys[n + 1:]]
    tag_id = youtube.tags.get(tag)
    video_list = youtube.search_video_by_category(tag_id)
    return render(request, 'treadweb/base_video.html',
                  {
                      'tag_list': tag_list,
                      'video_list': video_list
                  }
                  )
