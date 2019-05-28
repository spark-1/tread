from pytrends.request import TrendReq
import matplotlib.pyplot as plt
from datetime import datetime

class GoogleTrend(): # 구글 트렌드를 통해 정보를 가져오는 클래스

    def __init__(self, keyword, hl = 'ko', tz = '82', timeframe = 'today 5-y', cat = 0, geo = 'KR', gprop = ''): # 생성자 기본 설정 값
        self.hl = hl
        self.tz = tz
        self.keyword = keyword
        self.timeframe = timeframe
        self.cat = cat
        self.geo = geo
        self.gprop = gprop
        self.update_pytrend()
        self.update_payload()

    # Login to Google. Only need to run this once, the rest of requests will use the same session.
    def update_pytrend(self):
        self.pytrend = TrendReq(hl=self.hl, tz=self.tz)

    # Create payload and capture API tokens. Only needed for interest_over_time(), interest_by_region() & related_queries()
    def update_payload(self):
        self.pytrend.build_payload(kw_list=self.keyword, cat=self.cat, timeframe=self.timeframe, geo=self.geo, gprop=self.gprop)

    def set_pytrend(self, hl = 'None', tz = 'None'): # hl는 host language, tz는 time zone
        if hl != 'None': # ex) 'ko', 'en_US'
            self.hl = hl
        if tz != 'None': # ex) 82:한국, 360:미국
            self.tz = tz
        self.update_pytrend()
        self.update_payload()

    def set_payload(self, keyword = None, timeframe = 'None', cat = -1, geo = 'None', gprop = 'None'): # 키워드리스트, 타임프레임, 카테고리, 지역, 구글 프로퍼티
        if keyword != None :
            self.keyword = keyword
        if timeframe != 'None': # ex) 'all', 'today 5-y', 'today 3-m', 'now 7-d', 'now 1-H', '2018-05-20 2019-01-20'
            self.timeframe = timeframe
        if cat != -1:
            self.cat = cat
        if geo != 'None': # ex) 'KR', 'US', ''
            self.geo = geo
        if gprop != 'None': # ex) 'images', 'news', 'youtube', 'froogle'
            self.gprop = gprop
        self.update_payload()

    # Interest Over Time
    def interest_over_time(self):
        self.interest_over_time_df = self.pytrend.interest_over_time() # Returns pandas.Dataframe
        self.interest_over_time_df = self.interest_over_time_df.iloc[:, :self.keyword.__len__()] # 안쓰는 데이터 isPartial 제거
        self.interest_over_time_list = self.interest_over_time_df_to_list()
        return self.interest_over_time_list

    # Interest by Region
    def interest_by_region(self): # 지역별로 검색 비율을 알려준다
        self.interest_by_region_df = self.pytrend.interest_by_region()
        return self.interest_by_region_df

    # Related Queries, returns a dictionary of dataframes
    def related_queries(self): # 키워드 관련 검색어를 순위별로 알려준다
        self.related_queries_dict = self.pytrend.related_queries()
        return self.related_queries_dict

    # Get Google Top Charts
    def top_charts(self): # 카테고리 별로 검색어 상위 랭크 보기 근데 에러...
        self.top_charts_df = self.pytrend.top_charts(date=201812, cid='Online Video')
        return self.top_charts_df

    # Get Google Keyword Suggestions
    def suggestions(self, keyword = 'youtube'): # 키워드에 맞는 검색 제안 서비스 단일 키워드만 가능
        self.suggestions_dict = self.pytrend.suggestions(keyword=keyword)
        return self.suggestions_dict

    def show_interest_over_time(self): # 시간에 따른 검색 비율을 그래프로 보여준다
        num = 0.0
        plt.figure(figsize=(14, 4))
        plt.style.use('ggplot')  # 더 이쁘게 그려준다
        for key in self.keyword:
            num += 0.1
            plt.plot(self.interest_over_time_df[key], c=plt.cm.rainbow(num), label=key)
        plt.legend(bbox_to_anchor=(1, 1), loc=2)  # 라벨의 위치를 정해준다
        plt.show()

    def interest_over_time_df_to_list(self):  # interest_over_time_df의 데이터프레임 타입의 데이터를 리스트 타입으로 변환
        date = self.interest_over_time_df.index.tolist()
        for i in range(len(date)):
            date[i] = date[i].date().strftime("%Y-%m-%d")
        date.insert(0, 'x')
        data = []
        data.append(date)
        for key in self.keyword:
            y = self.interest_over_time_df[key].tolist()
            y.insert(0, key)
            data.append(y)
        return data

    def interest_by_region_df_to_list(self):  # interest_by_region_df의 데이터프레임 타입의 데이터를 리스트 타입으로 변환
        region = self.interest_by_region_df.index.tolist()
        data = []
        for key in self.keyword:
            y = self.interest_by_region_df[key].tolist()
        for i in range(len(region)):
            data.append([region[i], y[i]])
        return data

""" 사용 방법 예시 """
if __name__ == '__main__':
    keyword = ['피자']
    googletrend = GoogleTrend()
    googletrend.set_payload(keyword = keyword)
    #print(googletrend.interest_over_time())
    googletrend.interest_by_region()
    print(googletrend.interest_by_region_df_to_list())

"""
# Get Google Hot Trends data
trending_searches_df = pytrend.trending_searches() # 오류
print(trending_searches_df)
print()

import numpy as np
import datetime

date_list=np.array(interest_over_time_df.index)
datestart=np.where(date_list == np.datetime64(datetime.datetime(2019, 2, 22))) # 해당 날짜가 몇번째 인덱스인지 확인 가능하다
print(datestart)
print()
"""
