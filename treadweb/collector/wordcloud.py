import matplotlib.pyplot as plt
from wordcloud import WordCloud
from treadweb.collector.naverDataLab import NaverDataLab
import re


class TreadWordCloud():
    def draw_cloud(self, keyword, width=1000, height=600):
        naver = NaverDataLab()
        list = naver.associative_search(keyword)
        text = ''
        for i in range(len(list)):
            text += (list[i] + ' ')
        news = naver.getNewsTitle(keyword)

        if news != []:
            for i in range(len(news)):
                text += (news[i] + ' ')
        else:
            text += keyword

        # font_path
        wordcloud = WordCloud(font_path='SeoulNamsan.ttf',
                              background_color='white', width=width, height=height, max_font_size=1000)\
            .generate(text)
        fig, axes = plt.subplots(ncols=1, nrows=1)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        fig.savefig('treadweb/static/treadweb/img/wordcloud.png', format='png')

    def remove_tag(self, content):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', content)
        return cleantext
