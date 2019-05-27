import re
import requests
import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from dateutil import parser
import json

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36'}

class NaverDataLab():

    def remove_tag(self, content):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', content)
        return cleantext

    # 연관검색어를 리스트형태로 리턴
    def associative_search(self, keyword):
        url = 'https://search.naver.com/search.naver?where=nexearch&query=' + keyword
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'lxml')

        subkeywords = soup.select('._related_keyword_ul')

        result = []

        for tab in subkeywords:
            for i in range(len(tab.select('a'))):
                result.append(self.remove_tag(tab.select('a')[i].text))
        return result

    # 전체, 10대, 20대, 30대 검색어 순위를 보여주는 함수 (dict 형태로 리턴)
    # year, month, day, hour, min, second -> 정수 형태로 입력 (second는 입력 안하면 00초 일 때로 설정됨)
    # ex) naver_searchlist(2019, 5, 21, 23, 30, 0)
    def naver_searchlist(self, time):
        url = 'https://datalab.naver.com/keyword/realtimeList.naver?datetime=' + time
        response = requests.get(url, headers = headers)
        soup = BeautifulSoup(response.content, 'lxml')

        rank_tabs = soup.select('.keyword_rank')[0:4]

        result = {}

        for tab in rank_tabs:
            ranks = tab.select('.list .title')
            title = tab.select('.rank_title')[0].text
            result[title] = []
            i = 0
            for rank in ranks:
                if i < 10:
                    result[title].append(rank.text)
                    i += 1

        # for data in result:
        #     print(data)
        #     print(result[data])
        return result

    # 키워드의 검색 빈도를 시간 단위로 출력해주는 함수
    # ex) keyword_search("핸드폰", ["갤럭시", "아이폰"])
    # ex) keyword_search("핸드폰", ["갤럭시", "아이폰"],device='mo', age=['1','2'],gender='m')
    # mainKeyword -> 상위 주제어  ex) "유튜브"
    # keywords -> 하위 주제어 (최대 20개까지 입력 가능) ex) ["유튜버","먹방","ASMR"]
    # device -> 검색할 때 사용한 기기 통계 (입력 안하면 pc + mobile 결과 출력) ex) "pc" or "mo"
    # age -> 검색 연령대 설정 (입력 안하면 전 연령대 결과 출력, 여러 연령대 결과 출력하고 싶을 때는 ["1","2","3"] 이런 식으로 리스트 입력)
    # - 1: 0∼12세
    # - 2: 13∼18세
    # - 3: 19∼24세
    # - 4: 25∼29세
    # - 5: 30∼34세
    # - 6: 35∼39세
    # - 7: 40∼44세
    # - 8: 45∼49세
    # - 9: 50∼54세
    # - 10: 55∼59세
    # - 11: 60세 이상
    # gender -> 검색 성별 설정 (입력 안하면 male + female 결과 출력) ex) "m" or "f"
    def keyword_search(self, mainKeyword, device='', age='0', gender=''):
        client_id = "gDb5rUUUu3cNZt3fIhxy"
        client_secret = "HWP6j_9S6w"
        url = "https://openapi.naver.com/v1/datalab/search";
        endTime = datetime.now().date().strftime("%Y-%m-%d")
        startTime = (parser.parse(endTime) - timedelta(days=30)).strftime("%Y-%m-%d")

        body = "{\"startDate\":\"" + startTime + "\",\"endDate\":\"" + endTime + "\",\"timeUnit\":\"date\",\"keywordGroups\":[{\"groupName\":\"" + mainKeyword + "\",\"keywords\":["
        keywords = self.associative_search(mainKeyword)
        body += ("\"" + keywords[0] + "\"")
        for i in range(1, len(keywords)):
            body += (",\"" + keywords[i] + "\"")
        body += "]}]"

        if device != '':
            body += (",\"device\":\"" + device + "\"")

        if age != '0':
            if len(age) == 1:
                body += (",\"age\":\"" + age + "\"")
            else:
                body += (",\"age\":[\"" + age[0] + "\"")
                for i in range(1, len(age)):
                    body  += (",\"" + age[i] + "\"")
                body += "]"

        if gender != '':
            body += (",\"gender\":\"" + gender + "\"")
        body += "}"

        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id",client_id)
        request.add_header("X-Naver-Client-Secret",client_secret)
        request.add_header("Content-Type","application/json")
        response = urllib.request.urlopen(request, data=body.encode("utf-8"))
        rescode = response.getcode()
        if(rescode==200):
            response_body = response.read()
            tmp = response_body.decode('utf-8')
            ret = self.str_to_list(tmp, mainKeyword)
            return ret
        else:
            print("Error Code:" + rescode)

    # api 결과를 list 형태로 변환해주는 함수
    def str_to_list(self, str, keyword):
        d_list = ['x']
        v_list = [keyword]
        cnt = 0
        idx = 0
        tmp = str
        while idx != -1:
            idx = tmp.find("period")
            if idx == -1:
                break
            date = tmp[idx+9:idx+19]
            tmp = tmp[idx:]
            idx = tmp.find("ratio")
            if idx == -1:
                break
            value = tmp[idx+7:idx+11]
            if value[-1] == ',' or value[-1] == '}':
                value = value[0:-1]
            value = round((float(value)))
            tmp = tmp[idx:]
            d_list.append(date)
            v_list.append(value)
            cnt += 1
        ret = [d_list, v_list]
        return ret

if __name__=='__main__':
    naver = NaverDataLab()
    # a = naver.naver_searchlist('2019-05-01T10:30:00')
    a = naver.keyword_search("휴대폰")
    print(a)
