from core.webs import WebHots
import requests
import json
import time
from pymysql.converters import escape_str

class weibo(WebHots):
    def __init__(self):
        WebHots.__init__(self)

    def getCtx(self):
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
        }
        url = "https://weibo.com/ajax/side/hotSearch"
        res = requests.get(url, headers=header)
        if res.status_code != 200:
            print(f'errcode: {res.status_code}')
            print(res.text)
            self.obj.clear()
            return

        try:
            self.obj = json.loads(res.text, strict=False)
        except Exception as e:
            print(f'parse error:', e.args[0])
            self.obj.clear()
            return

    def parse(self):
        datas = list()
        for i in self.obj["data"]["realtime"]:
            # 跳过广告
            if 'ad_channel' in i:
                continue
            datas.append({
                "date": time.strftime("%Y-%m-%d", time.localtime()),
                "rank": i["realpos"],
                "title": escape_str(i['word']),
                "desc": escape_str(i['note']),
                "link": f'https://s.weibo.com/weibo?q=${i["word"]}&t=31&band_rank=1&Refer=top',
            })
        return datas

    def updateDB(self, res: list):
        for i in res:
            self.db.connect('hot')
            txt = f'''
            INSERT INTO
                weibo (query_date,ranking,title,link,descript)
            VALUES
                ('{i['date']}','{i['rank']}',{i['title']},'{i['link']}',{i['desc']})
            '''
            self.db.exec(txt)


if __name__ == '__main__':
    hot = weibo()
    hot.run()
