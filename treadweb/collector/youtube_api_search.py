
import json
from urllib import parse
import urllib.request
import json


class YoutubeSearch(object) :
    #분류별로 데이터들을 검색할 클래스

    def __init__(self,size):
        self.size = size; #각 검색요소당 결과로 나올 영상 개수
        self.__developer_key = "AIzaSyDJaA3yPXhSDKxYYu0DTLs1VSPMg1FlXxw"

    def get_view_count(self,channel_id):
        data=urllib.request.urlopen("https://www.googleapis.com/youtube/v3/channels?part=statistics&id={}&key={}".format(channel_id,self.__developer_key)).read()
        view_count = json.loads(data)["items"][0]["statistics"]["viewCount"]
        return view_count
        #채널의 총 조회수

    def search_keyword(self,keyword):
        #검색어를 조회수순으로 검색한 영상
        word = parse.quote(keyword)
        data = urllib.request.urlopen("https://www.googleapis.com/youtube/v3/search?part=snippet&q={}&order=viewCount&maxResults={}&key={}".format(word,self.size,self.__developer_key)).read()
        list = json.loads(data)["items"]
        response = list
        v_data : data = []
        for i in range(len(response)):
            v_data.append({
                'video_id': response[i]["id"],
                'publishedAt': response[i]["snippet"]["publishedAt"],
                'channel_id': response[i]["snippet"]["channelId"],
                'video_title': response[i]["snippet"]["title"],
                'description': response[i]["snippet"]["description"],
                'channel_title': response[i]["snippet"]["channelTitle"],
                'video_thumbnail' : response[i]["snippet"]["thumbnails"]["default"]["url"]
            })
        return v_data


    def search_video_orderby_view(self):
        #전체 조회수순으로 나열된 영상들의 배열을 v_data 개게 안에 리스트로 담아 넘깁니다
        data = urllib.request.urlopen("https://www.googleapis.com/youtube/v3/search?part=snippet&order=viewCount&maxResults={}&type=video&key={}".format(self.size,self.__developer_key)).read()
        list = json.loads(data)["items"]
        response = list
        v_data: data = []
        for i in range(len(response)):

            v_data.append({
                'video_id': response[i]["id"]["videoId"],
                'publishedAt': response[i]["snippet"]["publishedAt"],
                'channel_id': response[i]["snippet"]["channelId"],
                'video_title': response[i]["snippet"]["title"],
                'description': response[i]["snippet"]["description"],
                'channel_title': response[i]["snippet"]["channelTitle"],
                'video_thumbnail': response[i]["snippet"]["thumbnails"]["default"]["url"]
            })
        return v_data

    def search_channel_orderby_view(self):
        #전체채널을 전체 조회수로 검색
        data = urllib.request.urlopen(
            "https://www.googleapis.com/youtube/v3/search?part=snippet&order=viewCount&type=channel&maxResults={}&key={}".format(
                self.size,self.__developer_key)).read()
        list = json.loads(data)["items"]
        response = list
        v_data: data = []
        for i in range(len(response)):
            v_data.append({
                'publishedAt': response[i]["snippet"]["publishedAt"],
                'channel_id': response[i]["snippet"]["channelId"],
                'title': response[i]["snippet"]["title"],
                'description': response[i]["snippet"]["description"],
                'channel_title': response[i]["snippet"]["channelTitle"],
                'video_thumbnail': response[i]["snippet"]["thumbnails"]["default"]["url"]
            })

        return v_data


    def search_video_by_category(self,category_id):
        '''카테고리 id
            1 : Film & Animation
            2 : Autos & Vehicles
            10 : Music
            15 : Pets & Animals
            17 : Sports
            18 : short movies
            19 : Travel&Events
            20 : Gaming
            21 : Videoblogging
            22 : People & Blogs
            23 : Comedy
            24 : Entertainment
            25 : News & Politics
            26 : Howto & Style
            27 : Education
            28 : Science & Technology
            30 : Movie
            31 : Anime/Animation
            32 : Action/Advencture
            33 : Classics
            44 : Trailers'''
        #카테고리안에서 mostpopular한 영상들 리턴
        data = urllib.request.urlopen(
            "https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&chart=mostPopular&maxResults={}&videoCategoryId={}&key={}".format(self.size,category_id,self.__developer_key)).read()
        list = json.loads(data)["items"]
        response = list
        v_data : data = []
        for i in range(len(response)) :
             v_data.append({
                'video_id' : response[i]["id"],
                'publishedAt' : response[i]["snippet"]["publishedAt"],
                'channel_id' : response[i]["snippet"]["channelId"],
                'video_title' : response[i]["snippet"]["title"],
                'description' : response[i]["snippet"]["description"],
                'channel_title' : response[i]["snippet"]["channelTitle"],
                'view_count' : response[i]["statistics"]["viewCount"],
                'like_count' : response[i]["statistics"]["likeCount"],
                'dislike_count' : response[i]["statistics"]["dislikeCount"],
                'comment_count' : response[i]["statistics"]["commentCount"],
                'video_thumbnail': response[i]["snippet"]["thumbnails"]["default"]["url"]
             })
            #defaultAudioLanguage속성을 넣지 않은 영상들도 많아서 ko걸로 구분이 안됨
        return v_data


    def get_video_statistics(self,video_id):
        #비디오 통계가 담긴 딕셔너리 리턴
        url = urllib.request.urlopen(
            "https://www.googleapis.com/youtube/v3/videos?part=statistics&id={}&key={}".format(
                video_id, self.__developer_key)).read()
        data = json.loads(url)["items"]
        video_statistics = {}
        video_statistics["view_count"] = data[0]["statistics"]["viewCount"]
        video_statistics["like_count"] = data[0]["statistics"]["likeCount"]
        video_statistics["commnet_count"] = data[0]["statistics"]["commentCount"]

        return video_statistics




#youtube.set_channel_id('UCT-_4GqC-yLY1xtTHhwY0hA')
#