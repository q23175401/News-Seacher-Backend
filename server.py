from flask import Flask, jsonify, request, g
from news_searcher import NewsSearcher
import json

new_searcher = NewsSearcher()
app = Flask(__name__)

test_news = {
    "news_id": "news_1",
    "news_url": "https://news.pts.org.tw/article/433344",
    "news_title": "�p�G�A����o��data�A�A��client�ݨS���e��keyword",
    "news_content": "�p�G�A����o��data�A�A��client�ݨS���e��keyword�p�G�A����o��data�A�A��client�ݨS���e��keyword�p�G�A����o��data�A�A��client�ݨS���e��keyword",
    "news_date": "2019-5-31",
    "news_category": "�F�v"
}

test_news2 = {
    "news_id": "news_1",
    "news_url": "https://news.pts.org.tw/article/433344",
    "news_title": "�p�G�A����o��data�A�A��client�ݰe�Ӫ��OGET",
    "news_content": "�p�G�A����o��data�A�A��client�ݰe�Ӫ��OGET request�p�G�A����o��data�A�A��client�ݰe�Ӫ��OGET request�p�G�A����o��data�A�A��client�ݰe�Ӫ��OGET request",
    "news_date": "2019-5-31",
    "news_category": "�F�v"
}

defult_data = {"support": [test_news2, test_news2],"unsupport": [test_news2, test_news2, test_news2]}

@app.route('/')
def hello_world():
    return 'hello, it\'s an index page. '

@app.route('/homepage', methods=['GET', 'POST'])
def news_analyze():
    return_data = jsonify(defult_data)
    if(request.method == 'POST'): # Condition1: the client sent a POST request
        try:
            print(request.get_data())
            client_reqDataDecode = request.get_data().decode()      # 把讀進來的Byte 形式解碼
            json_clientPayloads = json.loads(client_reqDataDecode)  # 把解碼完的字串再根據Json的格式 輸出dictionary
            user_reqKeyword = json_clientPayloads['keyword']        # 從dictionary拿出 Keyword
            try:  # 嘗試拿時間
                time_range = {
                    "starttime": json_clientPayloads["starttime"],
                    "endtime": json_clientPayloads["endtime"],
                }
            except: # 拿失敗就算了
                time_range = None
            
            if time_range:  # 有時間的話 就輸出
                print("Get Uer KeyWord: {} with StartTime: {} EndTime: {}".format(user_reqKeyword, time_range["starttime"], time_range["endtime"]))
            else:           # 沒就算了
                print("Get Uer KeyWord: {}".format(user_reqKeyword))

            # 把Keyword time_range 放進去News Searcher 尋找相關的新聞
            return_dict = new_searcher.get_relevant_rank_list(user_reqKeyword, time_range)
            return_data = jsonify(return_dict)
        except Exception as e: # 看錯誤是啥
            print(e)
    return return_data

if __name__ == '__main__':
    #app.run(host="140.115.54.123", port=5000, debug=True)
    app.run(host="127.0.0.1", port=5000, debug=True, use_reloader=False)