import re
from jieba_tw_master import jieba as jiezh
import json


redundant_words = ['，',',','。','.','?','~','+','-','*','/','!','@','=','「','」','？','！','％','／','\u3000','\u200b','★',
                   '_','\\','#','<','>','&',';','》','《','：','◎',')','(',' ','\n','、','〉','〈',':','】','【','\r']


def cut_strip_data(one_data):
    cut_d = list( jiezh.cut(one_data,cut_all=False) )
    deal_d = [i for i in cut_d if i not in redundant_words]
    return deal_d

def get_dealed_data(news_title, news_content):
    content_sentences = re.split('，|\n|。', news_content)  # 根據標點符號把文章分成好幾個句子，但是會有空的list

    dealed_title = cut_strip_data(news_title)
    dealed_content = [cut_strip_data(sen) for sen in content_sentences if not len(sen)==0]
    
    return dealed_title, dealed_content