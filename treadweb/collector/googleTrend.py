from pytrends.request import TrendReq
import matplotlib.pyplot as plt
import random

class GoogleTrend(): # 구글 트렌드를 통해 정보를 가져오는 클래스

    def __init__(self, keyword = ['youtube'], hl = 'ko', tz = '82', timeframe = 'today 5-y', cat = 0, geo = 'KR', gprop = ''): # 생성자 기본 설정 값
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
        if timeframe != 'None': # ex) 'all', 'today 5-y', 'today 1,2,3-m', 'now 1,7-d', 'now 1,4-H', '2018-05-20 2019-01-20'
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

    # Interest Over Time hourly
    def historical_hourly_interest(self):
        self.historical_hourly_interest_df = self.pytrend.get_historical_interest(keywords=self.keyword, year_start=2019, month_start=4, day_start=1, hour_start=0, year_end=2019, month_end=5, day_end=1, hour_end=0, cat=0, geo='KR', gprop='', sleep=0)  # Returns pandas.Dataframe
        self.historical_hourly_interest_df = self.historical_hourly_interest_df.iloc[:, :self.keyword.__len__()]  # 안쓰는 데이터 isPartial 제거
        self.historical_hourly_interest_list = self.historical_hourly_interest_df_to_list()
        return self.historical_hourly_interest_list

    # Interest by Region
    def interest_by_region(self): # 지역별로 검색 비율을 알려준다
        self.interest_by_region_df = self.pytrend.interest_by_region()
        self.interest_by_region_list = self.interest_by_region_df_to_list()
        return self.interest_by_region_list

    # Related Topics, Returns dictionary of pandas.DataFrames
    def related_topics(self): # 키워드 관련 토픽을 순위별로 알려준다
        self.related_topics_dict = self.pytrend.related_topics()
        return self.related_topics_dict

    # Related Queries, returns a dictionary of dataframes
    def related_queries(self): # 키워드 관련 검색어를 순위별로 알려준다
        self.related_queries_dict = self.pytrend.related_queries()
        return self.related_queries_dict

    # trending searches in real time
    def trending_searches(self): # 현재 시간대 인기검색어 순위 20까지 보여준다
        self.trending_searches_df = self.pytrend.trending_searches(pn='south_korea')
        return self.trending_searches_df

    #
    def today_searches(self):  #
        self.today_searches_df = self.pytrend.today_searches()
        return self.today_searches_df

    # Get Google Top Charts
    def top_charts(self): # 년 단위로 상위 핫 키워드 가져오기
        self.top_charts_df = self.pytrend.top_charts(date=2015, hl='ko', tz='82', geo='KR') # date = YYYY integer, tz='82', geo='KR', geo='GLOBAL', geo='US'
        return self.top_charts_df

    # Get Google Category
    def categories(self): # 구글 카테고리 종류와 id를 보여준다
        self.categories_df = self.pytrend.categories()
        return self.categories_df

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

    def historical_hourly_interest_df_to_list(self):  # historical_hourly_interest_df의 데이터프레임 타입의 데이터를 리스트 타입으로 변환
        date = self.historical_hourly_interest_df.index.tolist()
        for i in range(len(date)):
            date[i] = date[i].date().strftime("%Y-%m-%d")
        date.insert(0, 'x')
        data = []
        data.append(date)
        for key in self.keyword:
            y = self.historical_hourly_interest_df[key].tolist()
            y.insert(0, key)
            data.append(y)
        return data

    def interest_by_region_df_to_list(self):  # interest_by_region_df의 데이터프레임 타입의 데이터를 리스트 타입으로 변환
        region = self.interest_by_region_df.index.tolist()
        data = []
        for key in self.keyword:
            y = self.interest_by_region_df[key].tolist()
        ratio = 0
        for i in [0, 1, 2, 3, 8, 11, 12, 13, 14, 15]:
            ratio += y[i]
        ratio /= 100
        tmp_val = 0
        reg_name = ''
        if ratio > 0:
            for i in range(len(region)):
                if i in [1, 2, 14, 11, 0, 13]:
                    if i == 0:
                        tmp_val = round(y[i] / ratio)
                        reg_name = '강원도'
                    elif i == 1:
                        tmp_val = round((y[i] + y[i + 1]) / ratio)
                        reg_name = '서울/경기'
                    elif i == 2:
                        tmp_val = round((y[i] + y[i + 1]) / ratio)
                        reg_name = '경상도'
                    elif i == 11:
                        tmp_val = round((y[i] + y[i + 1]) / ratio)
                        reg_name = '전라도'
                    elif i == 13:
                        tmp_val = round(y[i] / ratio)
                        reg_name = '제주도'
                    elif i == 14:
                        tmp_val = round((y[i] + y[i + 1]) / ratio)
                        reg_name = '충청도'
                    data.append([reg_name, tmp_val])
        return data

if __name__ == '__main__':
    keyword = ['햄버거']
    googletrend = GoogleTrend()
    googletrend.set_payload(keyword = keyword)
    #print(googletrend.interest_over_time())
    #print(googletrend.historical_hourly_interest())
    #print(googletrend.interest_by_region())
    #print(googletrend.related_topics())
    #print(googletrend.related_queries())
    #print(googletrend.trending_searches());
    #print(googletrend.today_searches());
    #print(googletrend.top_charts())
    #print(googletrend.categories())

