import re, os, sys, math, csv, json, random, operator
import pandas as pd
import numpy as np
from jieba_tw_master import jieba as jiezh
from NewsSearcherDB import NewsDB
from DealData import cut_strip_data
from gensim import corpora
from gensim.summarization import bm25

class NewsSearcher:
    def __init__(self):
        # 從我的Database拿全部的新聞資料， 要換可以隨時換別的 DB
        self.db = NewsDB()
        self.news_rows = self.db.get_all_news_list()  # 是一個list 根據 self.news_rows[ni][content]可以索引每行
        print("拿到總共 {} 筆資料".format(len(self.news_rows)))
        try:
            jiezh.enable_parallel(10)
        except:
            pass

        dealed_duc = []
        if os.path.isfile("all_dealed_doc.json"):
            with open("all_dealed_doc.json", 'r') as fp:
                news_dict_id = json.load(fp)
            for dealed_doc in news_dict_id.values():
                dealed_duc.append(dealed_doc)
        else:
            # 把所有資料都 cut_strip_data() 如果資料庫有已經整理過的內容會超快 因為結疤在windows下 不能開thread 不過如果是server的話可先開好
            for news_row in self.news_rows:
                d = list(cut_strip_data(news_row["title"])) + list(cut_strip_data(news_row["content"]))
                dealed_duc.append(d)

            # 把這個處理過的檔案存下來
            news_dict_id = {}
            for di, dealed_doc in enumerate(dealed_duc):
                news_dict_id[di] = dealed_doc
            with open("all_dealed_doc.json", 'w') as fp:
                json.dump(news_dict_id, fp)

        # BM25 model 如果資料都處理好的話 這個超快
        self.b25model = bm25.BM25(dealed_duc)
        self.average_idf = sum(map(lambda k: float(self.b25model.idf[k]), self.b25model.idf.keys())) / len(self.b25model.idf.keys())

    def get_relevant_rank_list(self, keyword, time_range=None):
        """
        把關鍵字分成支持跟不支持的關鍵字
        丟進BM25 model
        至於其他改進的 model 可以加在下面改動分數
        """
        keyword = list(jiezh.cut(keyword))
        support = ["支持"] + keyword
        unsupport = ["反對"] + keyword

        # support 的分數計算
        support_score_list = self.b25model.get_scores(support, average_idf = self.average_idf)
        # support_score_list = self.b25model.get_scores(support)
        support_score_dict = {}
        support_ID_time_dict = {}
        for ni, score in enumerate(support_score_list):
            support_score_dict[self.news_rows[ni]['ID']] = score  # 是根據這個news 的 id ，並不是根據比賽給的news_id ， 根據database中自動增加的id
            support_ID_time_dict[self.news_rows[ni]['ID']] = self.news_rows[ni]['time']

        sorted_all_news_scores_support = sorted(support_score_dict.items(), key=operator.itemgetter(1), reverse=True)
        support_result_news_id_list = [str(news_id_score_tuple[0]) for news_id_score_tuple in sorted_all_news_scores_support[:2000] if self.check_if_in_date_range(support_ID_time_dict[news_id_score_tuple[0]], time_range)]

        # unsupport 的分數計算
        unsupport_score_list = self.b25model.get_scores(unsupport, average_idf=self.average_idf)
        # unsupport_score_list = self.b25model.get_scores(unsupport)
        unsupport_score_dict = {}
        unsupport_ID_time_dict = {}
        for unni, unscore in enumerate(unsupport_score_list):
            unsupport_score_dict[self.news_rows[unni]['ID']] = unscore
            unsupport_ID_time_dict[self.news_rows[unni]['ID']] = self.news_rows[unni]['time']

        sorted_all_news_scores_unsupport = sorted(unsupport_score_dict.items(), key=operator.itemgetter(1), reverse=True)
        unsupport_result_news_id_list = [str(news_id_score_tuple[0]) for news_id_score_tuple in sorted_all_news_scores_unsupport[:2000] if self.check_if_in_date_range(unsupport_ID_time_dict[news_id_score_tuple[0]], time_range)]
        
        # 根據 兩種list 把 對應的資料回傳
        result_dict = {
            "support": self.db.select_by_row_id_list(support_result_news_id_list),
            "unsupport": self.db.select_by_row_id_list(unsupport_result_news_id_list)
        }
        return result_dict

    def translateFormalTime(self, time):
        times = time.split("-")
        year = times[0]
        month = times[1]
        day = times[2]
        return int(year), int(month), int(day)

    def time_less_than(self, fy, fm, fd, sy, sm, sd):
        if fy<sy:
            return True
        elif fy==sy:
            if fm<sm:
                return True
            elif fm==sm:
                if fd<=sd:
                    return True
        return False

    def check_if_in_date_range(self, news_time, date_range):
        """
        要檢查時間範圍有沒有包含這篇文章
        """
        if date_range!=None:
            start_year , start_month , start_day = self.translateFormalTime(date_range["starttime"])
            end_year   , end_month   , end_day   = self.translateFormalTime(date_range["endtime"])
            this_year  , this_month  , this_day  = self.translateFormalTime(news_time)
            
            if self.time_less_than(start_year, start_month, start_day, this_year, this_month, this_day) and \
             self.time_less_than(this_year, this_month, this_day, end_year, end_month, end_day):
                return True

            return False
        else:
            return True

    def __del__(self):
        del self.db


if __name__ == "__main__":
    NS = NewsSearcher()
    time_range = {
        "starttime": "2010-5-6",
        "endtime": "2019-5-6",
    }
    relevant_news = NS.get_relevant_rank_list("陳前總統保外就醫", None)
    print(relevant_news)