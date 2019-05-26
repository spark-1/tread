from pytrends.request import TrendReq
import matplotlib.pyplot as plt

class GoogleTrend(): # 구글 트렌드를 통해 정보를 가져오는 클래스

    def __init__(self, hl = 'en_US', tz = '360', keyword = ['youtube'], timeframe = 'today 5-y', cat = 0, geo = '', gprop = ''): # 생성자 기본 설정 값
        self.hl = hl
        self.tz = tz
        self.keyword = keyword
        self.timeframe = timeframe
        self.cat = cat
        self.geo = geo
        self.gprop = gprop
        self.update_pytrend()
        self.update_payload()

    def update_pytrend(self):
        self.pytrend = TrendReq(hl=self.hl, tz=self.tz)

    def update_payload(self):
        self.pytrend.build_payload(kw_list=self.keyword, cat=self.cat, timeframe=self.timeframe, geo=self.geo, gprop=self.gprop)

    def set_pytrend(self, hl, tz):
        self.hl = hl
        self.tz = tz
        self.update_pytrend()
        self.update_payload()

    def set_payload(self, keyword, timeframe, cat, geo, gprop):
        self.keyword = keyword
        self.timeframe = timeframe
        self.cat = cat
        self.geo = geo
        self.gprop = gprop
        self.update_payload()

    def set_language_to_korean(self): # 데이터의 키 값을 한국어로 설정한다
        self.hl='ko'
        self.pytrend = TrendReq(hl=self.hl, tz=self.tz)
        self.pytrend.build_payload(kw_list=self.keyword, cat=self.cat, timeframe=self.timeframe, geo=self.geo, gprop=self.gprop)

    def set_language_to_english(self): # 데이터의 키 값을 영어로 설정한다
        self.hl = 'en-US'
        self.pytrend = TrendReq(hl=self.hl, tz=self.tz)
        self.pytrend.build_payload(kw_list=self.keyword, cat=self.cat, timeframe=self.timeframe, geo=self.geo, gprop=self.gprop)

    def set_time_to_korea(self): # 정보의 시간대를 한국으로 설정한다
        self.tz = 82
        self.pytrend = TrendReq(hl=self.hl, tz=self.tz)
        self.pytrend.build_payload(kw_list=self.keyword, cat=self.cat, timeframe=self.timeframe, geo=self.geo, gprop=self.gprop)

    def set_time_to_us(self): # 정보의 시간대를 미국으로 설정한다
        self.tz = 360
        self.pytrend = TrendReq(hl=self.hl, tz=self.tz)
        self.pytrend.build_payload(kw_list=self.keyword, cat=self.cat, timeframe=self.timeframe, geo=self.geo, gprop=self.gprop)

    def set_keyword(self, keyword): # 검색할 키워드 리스트를 설정한다
        self.keyword = keyword
        self.pytrend.build_payload(kw_list=self.keyword, cat=self.cat, timeframe=self.timeframe, geo=self.geo, gprop=self.gprop)

    def set_timeframe_to_all(self):  # 탐색 시간 범위를 2004년부터 지금까지로 선택한다
        self.timeframe = 'all'
        self.pytrend.build_payload(kw_list=self.keyword, cat=self.cat, timeframe=self.timeframe, geo=self.geo, gprop=self.gprop)

    def set_timeframe_to_year(self):  # 탐색 시간 범위를 5년으로 선택한다
        self.timeframe = 'today 5-y'
        self.pytrend.build_payload(kw_list=self.keyword, cat=self.cat, timeframe=self.timeframe, geo=self.geo, gprop=self.gprop)

    def set_timeframe_to_month(self):  # 탐색 시간 범위를 3개월으로 선택한다
        self.timeframe = 'today 3-m'
        self.pytrend.build_payload(kw_list=self.keyword, cat=self.cat, timeframe=self.timeframe, geo=self.geo, gprop=self.gprop)

    def set_timeframe_to_week(self):  # 탐색 시간 범위를 일주일로 한다
        self.timeframe = 'now 7-d'
        self.pytrend.build_payload(kw_list=self.keyword, cat=self.cat, timeframe=self.timeframe, geo=self.geo, gprop=self.gprop)

    def set_timeframe_to_hour(self):  # 탐색 시간 범위를 한시간으로 한다
        self.timeframe = 'now 1-H'
        self.pytrend.build_payload(kw_list=self.keyword, cat=self.cat, timeframe=self.timeframe, geo=self.geo, gprop=self.gprop)

    def set_timeframe_user(self, timeframe):  # 탐색 시간 범위를 유저가 임의로 정한 시간 범위대로 한다 '2018-05-20 2019-01-20'
        self.timeframe = timeframe
        self.pytrend.build_payload(kw_list=self.keyword, cat=self.cat, timeframe=self.timeframe, geo=self.geo, gprop=self.gprop)

    def set_region_to_korea(self): # 탐색 지역을 한국으로 설정한다
        self.geo = 'KR'
        self.pytrend.build_payload(kw_list=self.keyword, cat=self.cat, timeframe=self.timeframe, geo=self.geo, gprop=self.gprop)

    def set_region_to_us(self):  # 탐색 지역을 미국으로 설정한다
        self.geo = 'US'
        self.pytrend.build_payload(kw_list=self.keyword, cat=self.cat, timeframe=self.timeframe, geo=self.geo, gprop=self.gprop)

    def set_region_to_world(self):  # 탐색 지역을 세계로 설정한다
        self.geo = ''
        self.pytrend.build_payload(kw_list=self.keyword, cat=self.cat, timeframe=self.timeframe, geo=self.geo, gprop=self.gprop)

    def set_property_to_images(self): # 이미지를 통해 검색한 키워드로 설정한다
        self.gprop = 'images'
        self.pytrend.build_payload(kw_list=self.keyword, cat=self.cat, timeframe=self.timeframe, geo=self.geo, gprop=self.gprop)

    def set_property_to_news(self): # 뉴스를 통해 검색한 키워드로 설정한다
        self.gprop = 'news'
        self.pytrend.build_payload(kw_list=self.keyword, cat=self.cat, timeframe=self.timeframe, geo=self.geo, gprop=self.gprop)

    def set_property_to_youtube(self): # 유튜브를 통해 검색한 키워드로 설정한다
        self.gprop = 'youtube'
        self.pytrend.build_payload(kw_list=self.keyword, cat=self.cat, timeframe=self.timeframe, geo=self.geo, gprop=self.gprop)

    def set_property_to_froogle(self): # 구글쇼핑을 통해 검색한 키워드로 설정한다
        self.gprop = 'froogle'
        self.pytrend.build_payload(kw_list=self.keyword, cat=self.cat, timeframe=self.timeframe, geo=self.geo, gprop=self.gprop)

    def interest_over_time(self): # 시간별로 검색 비율을 알려준다
        self.interest_over_time_df = self.pytrend.interest_over_time()
        self.interest_over_time_df = self.interest_over_time_df.iloc[:, :self.keyword.__len__()]
        return self.interest_over_time_df

    def interest_by_region(self): # 나라 혹은 지역별로 검색 비율을 알려준다
        self.interest_by_region_df = self.pytrend.interest_by_region()
        return self.interest_by_region_df

    def related_queries(self): # 키워드 관련 검색어를 순위별로 알려준다
        self.related_queries_dict = self.pytrend.related_queries()
        return self.related_queries_dict

    def top_charts(self): # 카테고리 별로 검색어 상위 랭크 보기 근데 에러...
        self.top_charts_df = self.pytrend.top_charts(date=201812, cid='Online Video')
        return self.top_charts_df

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

""" 사용 방법 예시 """

keyword = ['Pizza', 'Italian', 'Spaghetti', 'Breadsticks', 'Sausage']

googletrend = GoogleTrend()
#googletrend.set_region_to_us()
#googletrend.set_keyword(keyword)
#print(googletrend.suggestions())
googletrend.set_timeframe_user('2018-05-20 2019-01-20')
googletrend.set_property_to_youtube()
print(googletrend.interest_over_time())
googletrend.set_payload(gprop="news")
print(googletrend.interest_over_time())
#googletrend.show_interest_over_time()



""" 함수들 설명 """
"""
# Login to Google. Only need to run this once, the rest of requests will use the same session.
pytrend = TrendReq(hl='en-US', tz=360) # hl은 host language로 en-US는 영어를 의미를 의미함, tz는 time zone으로 360은 US CST를 의미함

# Create payload and capture API tokens. Only needed for interest_over_time(), interest_by_region() & related_queries()
keyword = ['Pizza', 'Italian', 'Spaghetti', 'Breadsticks', 'Sausage'] # 검색할 키워드를 정의
pytrend.build_payload(kw_list = keyword, cat=0, timeframe='today 3-m', geo='KR', gprop='') # 파라미터 순서대로 키워드리스트, 카테고리, 타임프레임, 나라, 구글 프로퍼티(이미지, 검색, 뉴스, 유튜브, 구글쇼핑)

# Interest Over Time
interest_over_time_df = pytrend.interest_over_time() # Returns pandas.Dataframe
interest_over_time_df = interest_over_time_df.iloc[:,:5] # 안쓰는 데이터 isPartial 제거
print(interest_over_time_df)
print()

# Interest by Region
interest_by_region_df = pytrend.interest_by_region() # geo가 default면 즉 세계이면 나라별로 보여주고, 나라이면 도시별로 보여준다
print(interest_by_region_df)
print()

# Related Queries, returns a dictionary of dataframes
related_queries_dict = pytrend.related_queries() # 관련 검색어와 빈도율을 리턴해준다.
print(related_queries_dict)
print()

# Get Google Hot Trends data
trending_searches_df = pytrend.trending_searches() # 오류
print(trending_searches_df)
print()

# Get Google Top Charts
top_charts_df = pytrend.top_charts(date='201611') # 오류
print(top_charts_df)
print()

# Get Google Keyword Suggestions
suggestions_dict = pytrend.suggestions(keyword='pizza')
print(suggestions_dict)
print() 

import numpy as np
import datetime

date_list=np.array(interest_over_time_df.index)
datestart=np.where(date_list == np.datetime64(datetime.datetime(2019, 2, 22))) # 해당 날짜가 몇번째인지 확인 가능하다
print(datestart)
print()

import matplotlib.pyplot as plt
plt.style.use('ggplot')
plt.plot(cointrenddf.index,cointrendT,c='m', label="Google Trend")
plt.plot(cointrenddf.index,coinpriceT,c='g', label="Bitcoin Historical Price")
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.show()
"""