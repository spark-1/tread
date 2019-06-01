from urllib import parse
import urllib.request
import json

class ChannelInfo :
    #검색한 데이터들에서 정보를 가져오는 클래스
    channel_tags = {'전체': 0, '영화': 1, '음악': 10, '스포츠': 17, '펫': 15, '게임': 20, '여행': 19, '브이로그': 21,
                    '코믹': 23, '엔터테인먼트': 24, '뉴스': 25, '뷰티': 26, '교육': 27, '과학기술': 28, '액션': 32, '애니메이션': 31}

    def __init__(self):
        pass
      #channel_data로 채널 정보, video 정보들 string으로 받을 수 있음
      #channel_data["video_list"]["index"]["video_statistics"]["viewCount"]로

    def load_channel_data(self, channel_id):
        #채널 정보들이 담겨진 channel_data 딕셔너리 리턴
        self.channel_id = channel_id
        self.__developer_key = "AIzaSyDJaA3yPXhSDKxYYu0DTLs1VSPMg1FlXxw"
        channel_data = {}
        channel_data["title"] = self.get_channel_title();
        channel_data["publishedaAt"] = self.get_channel_publishedAt()
        channel_data["description"] = self.get_description()
        channel_data["thumbnails"] = self.get_thumbnails()
        channel_data["subscriber"] = self.get_subscriber_count()
        channel_data["view_count"] = self.get_view_count()
        channel_data['video_count'] = self.get_video_count()

        return channel_data

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
        return self.convert_numeric_unit(channel_view)

    def get_subscriber_count(self):
        url = urllib.request.urlopen(
            "https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&id={}&key={}".format(
                self.channel_id, self.__developer_key)).read()
        channel_subscriber = json.loads(url)["items"][0]["statistics"]["subscriberCount"]
        return self.convert_numeric_unit(channel_subscriber)

    def get_video_count(self):
        #채널이 가진 비디오 수 리턴
        url = urllib.request.urlopen(
            "https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&id={}&key={}".format(
                self.channel_id, self.__developer_key)).read()
        channel_video_count = json.loads(url)["items"][0]["statistics"]["videoCount"]
        return self.convert_numeric_unit(channel_video_count)

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

        for i in range(len(data)) :
            if data[i]["id"].get("videoId"):
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

    def convert_numeric_unit(self, number):
        num = int(number)
        if num >= 100000000:
            return str(num // 100000000) + "억"
        elif num >= 1000000:
            return str(num // 1000000) + "백만"
        elif num >= 10000:
            return str(num // 10000) + "만"
        else:
            return str(num);
