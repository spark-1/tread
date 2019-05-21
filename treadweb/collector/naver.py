import requests
import urllib.request
from bs4 import BeautifulSoup

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36'}

# 전체, 10대, 20대, 30대 검색어 순위를 보여주는 함수 (dict 형태로 리턴)
# year, month, day, hour, min, second -> 정수 형태로 입력 (second는 입력 안하면 00초 일 때로 설정됨)
# ex) naver_searchlist(2019, 5, 21, 23, 30, 0)
def naver_searchlist(year, month, day, hour, minute, second=0):
    if month < 10:
        month = '0' + str(month)
    if day < 10:
        day = '0' + str(day)
    if hour < 10:
        hour = '0' + str(hour)
    if minute < 10:
        minute = '0' + str(minute)
    if second < 10:
        second = '0' + str(second)

    time = str(year) + '-' + str(month) + '-' + str(day) + 'T' + str(hour) + ':' + str(minute) + ':' + str(second)

    url = 'https://datalab.naver.com/keyword/realtimeList.naver?datetime=' + time
    response = requests.get(url, headers = headers)
    soup = BeautifulSoup(response.content, 'lxml')

    rank_tabs = soup.select('.keyword_rank')[0:4]

    result = {}

    for tab in rank_tabs:
        ranks = tab.select('.list .title')
        title = tab.select('.rank_title')[0].text
        result[title] = []

        for rank in ranks:
            result[title].append(rank.text)

    # for data in result:
    #     print(data)
    #     print(result[data])
    return result

# 키워드 시간 단위별로 검색 빈도 출력 함수
# ex) keyword_search("2018-05-01", "2019-04-01", "month", "핸드폰", ["갤럭시", "아이폰"],device='mo', age=['1','2'],gender='m')
# startTime, endTime -> yyyy-MM-dd 형식으로 사용
# timeUnit -> month, week, day 중 택 1
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
def keyword_search(startTime, endTime, timeUnit, mainKeyword, keywords, device='', age='0', gender=''):
    client_id = "gDb5rUUUu3cNZt3fIhxy"
    client_secret = "HWP6j_9S6w"
    url = "https://openapi.naver.com/v1/datalab/search";
    body = "{\"startDate\":\"" + startTime + "\",\"endDate\":\"" + endTime + "\",\"timeUnit\":\"" + timeUnit + "\",\"keywordGroups\":[{\"groupName\":\"" + mainKeyword + "\",\"keywords\":["
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
        return response_body.decode('utf-8')
    else:
        print("Error Code:" + rescode)


if __name__=='__main__':
    a = naver_searchlist(2019, 5, 21, 23, 30, 0)
    print(a['전체 연령대'])
    print(keyword_search("2018-05-01", "2019-04-01", "month", "핸드폰", ["갤럭시", "아이폰"], device='mo', age=['1', '2'], gender='m'))