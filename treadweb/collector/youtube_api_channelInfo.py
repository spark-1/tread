from urllib import parse
import urllib.request
import json
from .youtube_api_search import Youtube_search

class channel_info :
    #검색한 데이터들에서 정보를 가져오는 클래스
    channel_data = {}

    def __init__(self,channel_id) :

        self.channel_id = channel_id
        self.__developer_key = "AIzaSyDJaA3yPXhSDKxYYu0DTLs1VSPMg1FlXxw"
        self.channel_data["channel_title"] = self.get_channel_title();
        self.channel_data["channel_publishedaAt"] = self.get_channel_publishedAt()
        self.channel_data["channel_description"] = self.get_description()
        self.channel_data["channel_thumbnails"] = self.get_thumbnails()
        self.channel_data["channel_subscriber"] = self.get_subscriber_count()
        self.channel_data["channel_view_count"] = self.get_view_count()
        self.channel_data["video_list"] = self.get_video_data()
      #channel_data로 채널 정보, video 정보들 string으로 받을 수 있음
      #channel_data["video_list"]["index"]["video_statistics"]["viewCount"]로

    def load_channel_data(self):
        #채널 정보들이 담겨진 channel_data 딕셔너리 리턴
        return self.channel_data

    def set_channel_id(self,channel_id):
        #채널 id 변경
        self.channel_id = channel_id;

    def get_channel_title(self) :
        #채널명 리턴
        url = urllib.request.urlopen("https://www.googleapis.com/youtube/v3/channels?part=id,snippet,statistics&id={}&key={}".format(self.channel_id,self.__developer_key)).read()
        data = json.loads(url)["items"]
        channel_title = data[0]["snippet"]["title"]
        return channel_title


    def get_channel_publishedAt(self):
        #채널 생긴 날짜 리턴
        url = urllib.request.urlopen(
            "https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&id={}&key={}".format(
                self.channel_id, self.__developer_key)).read()
        channel_pusblished = json.loads(url)["items"][0]["snippet"]["publishedAt"]
        return channel_pusblished

    def get_description(self):
        #채널 설명 리턴
        url = urllib.request.urlopen(
            "https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&id={}&key={}".format(
                self.channel_id, self.__developer_key)).read()
        channel_description = json.loads(url)["items"][0]["snippet"]["description"]
        return channel_description

    def get_thumbnails(self):
        #채널 썸네일 리턴
        url = urllib.request.urlopen(
            "https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&id={}&key={}".format(
                self.channel_id, self.__developer_key)).read()
        channel_thumbnails = json.loads(url)["items"][0]["snippet"]["thumbnails"]["default"]["url"]
        return channel_thumbnails

    def get_view_count(self):
        #채널 전체 조회수 리턴
        url = urllib.request.urlopen(
            "https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&id={}&key={}".format(
                self.channel_id, self.__developer_key)).read()
        channel_view = json.loads(url)["items"][0]["statistics"]["viewCount"]
        return channel_view

    def get_subscriber_count(self):
        url = urllib.request.urlopen(
            "https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&id={}&key={}".format(
                self.channel_id, self.__developer_key)).read()
        channel_subscriber = json.loads(url)["items"][0]["statistics"]["subscriberCount"]
        return channel_subscriber

    def get_video_count(self):
        #채널이 가진 비디오 수 리턴
        url = urllib.request.urlopen(
            "https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&id={}&key={}".format(
                self.channel_id, self.__developer_key)).read()
        channel_video_count = json.loads(url)["items"][0]["statistics"]["videoCount"]
        return channel_video_count

    def get_playlists(self):
        #채널이 가진 플레이리스트 리턴
        url = urllib.request.urlopen(
            "https://www.googleapis.com/youtube/v3/playlists?part=snippet&channelId={}&key={}".format(
                self.channel_id, self.__developer_key)).read()
        p_data = json.loads(url)["items"]
        channel_playlist = []
        for i in range(len(p_data)) :
            channel_playlist.append(p_data[i])
        return channel_playlist

    def get_video_data(self):
        #채널이 가진 영상정보를 가진 배열 객체를 리턴
        url = urllib.request.urlopen("https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={}&order=viewCount&key={}".format(self.channel_id,self.__developer_key)).read()
        data = json.loads(url)["items"]
        video_list : url = []

        for i in range(5) :
            video_statiscs = self.get_video_statistics(data[i]["id"]["videoId"])
            video_list.append({
                'publishedAt' : data[i]["snippet"]["publishedAt"],
                'video_id' : data[i]["id"]["videoId"],
                'video_title' : data[i]["snippet"]["title"],
                'video_description' : data[i]["snippet"]["description"],
                'video_thumbnails' : data[i]["snippet"]["thumbnails"],
                'video_statistics' : video_statiscs
            })

        return video_list

    def get_video_statistics(self, video_id):
        # 비디오 통계가 담긴 딕셔너리 리턴
        url = urllib.request.urlopen(
            "https://www.googleapis.com/youtube/v3/videos?part=statistics&id={}&key={}".format(
                video_id, self.__developer_key)).read()
        data = json.loads(url)["items"]
        video_statistics = {}
        video_statistics["view_count"] = data[0]["statistics"]["viewCount"]
        video_statistics["like_count"] = data[0]["statistics"]["likeCount"]
        video_statistics["commnet_count"] = data[0]["statistics"]["commentCount"]

        return video_statistics




youtube_api = Youtube_search(5)
video_list = youtube_api.search_video_by_category(20) #카테고리분류별의 비디오 리스트를 받는다
for video in video_list:
    print(video)
#비디오 리스트의 첫번째 비디오 딕셔너리를 받아오고
print(video_list[0]["video_title"])
print(video_list[0]["like_count"]) #publishedAt, channel_id, video_title, description, channel_title, view_count, like_count, dislike_count, comment_count 등의 키값을 넣어 밸류를 받을 수 있습니다
                                 #이미 영상을 받아온 거라 이 클래스의 video 함수들을 사용할 필요가 없습니다
print(video_list[0]["channel_title"]) #이 비디오의 채널정보를 알고 싶을 때만 channel_info 클래스를 사용ㅎ면 됩니다.


channel_list = youtube_api.search_video_orderby_view() #그 외에 조회수 순으로 나열된 영상들의 리스트를 받으면
print(channel_list[0]["channel_title"])   #인덱스 다음값에 publishedAt, channel_id, video_title, description, channel_title등의 키값을 넣어서 기본적인 정보들은 받을 수 있습니다
                                          #by_category 함수 말고는 다 statistics 정보는 딕셔너리 안에 없으므로 channel_info의 get_video_statistics 함수를 이용해야 가져올 수 있습니다

channel = youtube_api.get_video_statistics(channel_list[0]["video_id"])  #video_id를 넣어서 비디오의 statistics를 가져옵니다
print(channel)


data = channel_info(channel_list[0]["channel_id"])
channel_data = data.load_channel_data() #load_data를 사용하여 channel_data 딕셔너리를 가져오면 모든 값을 받을 수 있음
print(channel_data["channel_title"])
print(channel_data["video_list"][0]["video_title"])
print(channel_data["video_list"][0]["video_statistics"]["view_count"])
print(channel_data["video_list"][0]["video_statistics"]["like_count"])
