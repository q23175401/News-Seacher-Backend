import sqlite3

class NewsDB:
    def __init__(self):
        try:
            self.db = sqlite3.connect("EchoChamber_DB.sqlite", check_same_thread=False)
            self.db.row_factory = sqlite3.Row
            self.cur = self.db.cursor()
            print("Database Connected")
        except:
            print("Database Connect Failed")
    def get_all_news_list(self):
        self.cur.execute("SELECT * FROM news")
        news_rows = self.cur.fetchall()

        self.cur.execute("SELECT * FROM ptt")
        ptt_rows = self.cur.fetchall()

        self.cur.execute("SELECT * FROM dcard")
        dcard_rows = self.cur.fetchall()

        all_news_list = list(news_rows) + list(ptt_rows) + list(dcard_rows)
        return [dict(i) for i in all_news_list]

    def select_by_row_id_list(self, row_id):
        select_id_string = ", ".join(row_id)

        self.cur.execute("SELECT * FROM news WHERE _rowid_ IN ({})".format(select_id_string))
        news_rows = self.cur.fetchall()

        self.cur.execute("SELECT * FROM ptt WHERE _rowid_ IN ({})".format(select_id_string))
        ptt_rows = self.cur.fetchall()

        self.cur.execute("SELECT * FROM dcard WHERE _rowid_ IN ({})".format(select_id_string))
        dcard_rows = self.cur.fetchall()

        all_news_list = list(news_rows) + list(ptt_rows) + list(dcard_rows)
        return [dict(i) for i in all_news_list]

    def __del__(self):
        self.db.close()

if __name__ == "__main__":
    db = NewsDB()
    # all_news = db.get_all_news_list()
    # print(all_news[db.news_id_range[1]-1][4])
    # print(all_news[db.ptt_id_range[1]-1][4])
    # print(all_news[db.dcard_id_range[1]-1][4])
    all_news = db.select_by_row_id_list(["10001" , "106619", "1"])
    print(all_news[2]["ID"])
