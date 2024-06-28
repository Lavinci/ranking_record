from core.webs import WebHots
import requests
import json
import time
from pymysql.converters import escape_str


class bilibili(WebHots):
    def __init__(self):
        WebHots.__init__(self)

    def getCtx(self):
        header = {
            "Origin": "https://www.bilibili.com",
            "Referer": "https://www.bilibili.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
        }
        url = "https://api.bilibili.com/x/web-interface/ranking/v2?type=all"
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

        if self.obj["code"] != 0:
            print(self.obj)
            self.obj.clear()

    def parse(self):
        datas = list()
        for x, i in enumerate(self.obj["data"]["list"]):
            datas.append({
                "date": time.strftime("%Y-%m-%d", time.localtime()),
                "rank": x,
                "title": escape_str(i['title']),
                "desc": escape_str(i['desc']),
                "link": i['short_link_v2'],
            })
        return datas

    def updateDB(self, res: list):
        name = "bilibili"
        for i in res:
            self.db.connect('hot')
            txt = f'''
            INSERT INTO {name} (query_date,ranking,title,link,descript)
            SELECT * FROM (
                SELECT "{i['date']}" AS query_date,
                "{i['rank']}" AS ranking,
                {i['title']} AS title,
                "{i['link']}" AS link,
                {i['desc']} AS descript
            ) as tmp
            WHERE NOT EXISTS(
                SELECT query_date, ranking from {name}
                WHERE query_date="{i['date']}" AND ranking="{i['rank']}"
            );
            '''
            # print(txt)
            self.db.exec(txt)


if __name__ == '__main__':
    hot = bilibili()
    hot.run()
