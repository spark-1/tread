from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_protect
from .collector.naverDataLab import NaverDataLab
from .collector.googleTrend import GoogleTrend
from datetime import datetime
from .collector.youtube_api_channelInfo import ChannelInfo
from .collector.youtube_api_search import YoutubeSearch
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
    youtube = YoutubeSearch()
    tag_keys = list(youtube.tags.keys())
    n = len(tag_keys) // 2
    tag_list = [tag_keys[i * n:(i+1) * n] for i in range((len(tag_keys) + n - 1) // n)]
    channels = youtube.search_channel_orderby_view();
    channel_list = []
    channel_info = ChannelInfo()
    for channel in channels:
        channel_data = channel_info.get_channel_data(channel["channel_id"])
        channel_list.append(channel_data)

    return render(request, 'treadweb/base_channel.html',
                  {
                      'tag_list': tag_list,
                      'channel_list': channel_list
                    }
                  )

def channel_tag(request, tag):
    youtube = YoutubeSearch()
    tag_keys = list(youtube.tags.keys())
    n = len(tag_keys) // 2
    tag_list = [tag_keys[i * n:(i + 1) * n] for i in range((len(tag_keys) + n - 1) // n)]

    channels = youtube.search_channel_orderby_view();
    channel_list = []
    channel_info = ChannelInfo()
    for channel in channels:
        channel_data = channel_info.get_channel_data(channel["channel_id"])
        channel_list.append(channel_data)
    return render(request, 'treadweb/base_channel.html',
                  {
                      'tag_list': tag_list,
                      'channel_list': channel_list
                  })

def video_page(request):
    youtube = YoutubeSearch()
    tag_keys = list(youtube.tags.keys())
    n = len(tag_keys) // 2
    tag_list = [tag_keys[i * n:(i+1) * n] for i in range((len(tag_keys) + n - 1) // n)]
    video_list = youtube.search_video_by_category(0)
    return render(request, 'treadweb/base_video.html',
                  {
                      'tag_list': tag_list,
                      'video_list': video_list
                    }
                  )


def video_tag(request, tag):
    return render(request, 'treadweb/base_video.html')
