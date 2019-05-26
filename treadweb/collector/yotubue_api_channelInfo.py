from urllib import parse
import urllib.request
import json
from . import youtube_api_search


class channel_info :
    #검색한 데이터들에서 정보를 가져오는 클래스

    def __init__(self,channel_id) :
        self.channel_id = channel_id
        self.__developer_key = "AIzaSyDJaA3yPXhSDKxYYu0DTLs1VSPMg1FlXxw"

    def load_data(self):
        info = dict()
        info['title'] = self.get_channel_title()
        return info

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
        channel_pusblished = json.loads(self.url)["items"][0]["snippet"]["publishedAt"]
        return channel_pusblished

    def get_description(self):
        #채널 설명 리턴
        url = urllib.request.urlopen(
            "https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&id={}&key={}".format(
                self.channel_id, self.__developer_key)).read()
        channel_description = json.loads(self.url)["items"][0]["snippet"]["description"]
        return channel_description

    def get_thumbnails(self):
        #채널 썸네일 리턴
        url = urllib.request.urlopen(
            "https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&id={}&key={}".format(
                self.channel_id, self.__developer_key)).read()
        channel_thumbnails = json.loads(url)["items"][0]["snippet"]["thumbnails"]
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

    def get_video(self):
        #채널이 가진 영상을 조회수 순으로 리턴
        url = urllib.request.urlopen("https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={}&order=viewCount&key={}".format(self.channel_id,self.__developer_key)).read()
        data = json.loads(url)["items"]
        video_list : url = []
        for i in range(5) :
            video_list.append({
                'publishedAt' : data[i]["snippet"]["publishedAt"],
                'video_id' : data[i]["id"]["videoId"],
                'video_title' : data[i]["snippet"]["title"],
                'video_description' : data[i]["snippet"]["description"],
                'video_thumbnails' : data[i]["snippet"]["thumbnails"],
            })

        return video_list


    def get_video_statistics(self,video_id):
        #비디오 통계 정보 리턴
        url = urllib.request.urlopen(
            "https://www.googleapis.com/youtube/v3/videos?part=snippet&channelId={}&order=viewCount&key={}".format(
                self.channel_id, self.__developer_key)).read()
        data = json.loads(url)["items"]
        video_statistics = []
        video_statistics.append({
            'view_couont' : data[0]["viewCount"],
            'like_count' : data[0]["likeCount"],
            'comment_count' : data[0]["commentCount"]
        })

        return video_statistics



if __name__=='__main__':
    youtube_api = youtube_api_search.Youtube_search(5)
    data = youtube_api.search_keyword("방탄소년단")
    channel_id = []
    for i in range(len(data)) :
        channel_id.append(data[i]["channel_id"])

    youtube_api_info = channel_info(channel_id[0])
    subscriber = youtube_api_info.get_subscriber_count()
    print(subscriber)
