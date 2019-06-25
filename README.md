#News Searcher Backend

這是用python3 寫的News Searcher

說明:
  1. 給定關鍵字，可以在資料庫中快速比對立場相同與相反的新聞
  2. 並且丟給使用者的APP當中，做統計分析
  3. 這是接收使用者request利用flase framework建立的http server

程式說明:
  1. 將資料庫的文章做分詞處理，分詞工具是利用jieba-tw-master，進行漢字的分詞
  2. 透過使用者的post requst取得前端使用著搜尋的關鍵字及時間範圍
  3. 再利用BM25 tg-idf model，將資料庫的新聞做相似度的分析
  4. 最後整理出在相對應時間範圍內的新聞，回傳給使用者
  

使用工具:
  1. jieba-tw-master : https://github.com/APCLab/jieba-tw
  2. flask
  3. sqlite3
