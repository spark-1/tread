from urllib import parse
import urllib.request
import json

# 검색한 데이터들에서 정보를 가져오는 클래스
class ChannelInfo :

    def __init__(self):
        f = open('tread_privacy.txt', mode='tr', encoding='utf-8')
        self.__developer_key = f.read().split('=')[1]
      #channel_data로 채널 정보, video 정보들 string으로 받을 수 있음
      #channel_data["video_list"]["index"]["video_statistics"]["viewCount"]로

    def get_channel_data(self, channel_id):
        #채널 정보들이 담겨진 channel_data 딕셔너리 리턴
        self.channel_id = channel_id
        self.load_channel_data(channel_id)
        channel_data = {}
        channel_data["title"] = self.get_channel_title();
        channel_data["publishedaAt"] = self.get_channel_publishedAt()
        channel_data["description"] = self.get_description()
        channel_data["thumbnails"] = self.get_thumbnails()
        channel_data["subscriber"] = self.get_subscriber_count()
        channel_data["view_count"] = self.get_view_count()
        channel_data['video_count'] = self.get_video_count()

        return channel_data

    def load_channel_data(self, channel_id):
        url = urllib.request.urlopen(
            "https://www.googleapis.com/youtube/v3/channels?part=id,snippet,statistics&id={}&key={}".format(
                channel_id, self.__developer_key)).read()
        self.data = json.loads(url)["items"]

    def set_channel_id(self,channel_id):
        #채널 id 변경
        self.channel_id = channel_id;

    def get_channel_title(self) :
        #채널명 리턴
        channel_title = self.data[0]["snippet"].get("title")
        return channel_title


    def get_channel_publishedAt(self):
        #채널 생긴 날짜 리턴
        channel_pusblished = self.data[0]["snippet"].get("publishedAt")
        return channel_pusblished

    def get_description(self):
        #채널 설명 리턴
        channel_description = self.data[0]["snippet"].get("description")
        return channel_description

    def get_thumbnails(self):
        #채널 썸네일 리턴
        channel_thumbnails = self.data[0]["snippet"]["thumbnails"]["default"].get("url")
        return channel_thumbnails

    def get_view_count(self):
        #채널 전체 조회수 리턴
        channel_view = self.data[0]["statistics"].get("viewCount")
        return self.convert_numeric_unit(channel_view)

    def get_subscriber_count(self):
        channel_subscriber = self.data[0]["statistics"].get("subscriberCount")
        return self.convert_numeric_unit(channel_subscriber)

    def get_video_count(self):
        #채널이 가진 비디오 수 리턴
        channel_video_count = self.data[0]["statistics"].get("videoCount")
        return self.convert_numeric_unit(channel_video_count)

    def get_playlists(self, channel_id):
        #채널이 가진 플레이리스트 리턴
        url = urllib.request.urlopen(
            "https://www.googleapis.com/youtube/v3/playlists?part=snippet&channelId={}&key={}".format(
                channel_id, self.__developer_key)).read()
        p_data = json.loads(url)["items"]
        channel_playlist = []
        for i in range(len(p_data)) :
            channel_playlist.append(p_data[i])
        return channel_playlist

    def get_video_data(self, channel_id):
        #채널이 가진 영상정보를 가진 배열 객체를 리턴
        url = urllib.request.urlopen("https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={}&order=viewCount&key={}".format(channel_id,self.__developer_key)).read()
        data = json.loads(url)["items"]
        video_list : url = []

        for i in range(len(data)) :
            if data[i]["id"].get("videoId"):
                video_statiscs = self.get_video_statistics(data[i]["id"]["videoId"])
                video_list.append({
                    'publishedAt' : data[i]["snippet"].get("publishedAt"),
                    'video_id' : data[i]["id"].get("videoId"),
                    'video_title' : data[i]["snippet"].get("title"),
                    'video_description' : data[i]["snippet"].get("description"),
                    'video_thumbnails' : data[i]["snippet"].get("thumbnails"),
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
        video_statistics["view_count"] = data[0]["statistics"].get("viewCount")
        video_statistics["like_count"] = data[0]["statistics"].get("likeCount")
        video_statistics["commnet_count"] = data[0]["statistics"].get("commentCount")

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
