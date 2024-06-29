from core.webs import WebHots
from core.utils import parseJson
import requests
import time
from pymysql.converters import escape_str


class bilibili(WebHots):
    def __init__(self):
        WebHots.__init__(self)
        self._352 = False

    def getCtx(self):
        header = {
            "Referer": "https://www.bilibili.com/ranking/all",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        }
        url = "https://api.bilibili.com/x/web-interface/ranking/v2?rid=0&type=all"
        res = requests.get(url, headers=header)
        if res.status_code != 200:
            print(f'errcode: {res.status_code}')
            print(res.text)
            self.obj.clear()
            return
        # print(res.text)
        self.obj = parseJson(res.text)
        if len(self.obj) == 0:
            return

        if self.obj["code"] == -352:
            print("触发风控,使用备用api")
            bak_url = "https://api.bilibili.com/x/web-interface/ranking?jsonp=jsonp?rid=0&type=1&callback=__jp0"
            res = requests.get(bak_url, headers=header)
            # print(res.text)
            self.obj = parseJson(res.text)
            if len(self.obj) == 0:
                return
            self._352 = True

        elif self.obj["code"] != 0:
            print(self.obj)
            self.obj.clear()

    def parse(self):
        datas = list()
        if not self._352:
            for x, i in enumerate(self.obj["data"]["list"]):
                rank = x + 1
                title = i["title"]
                print(f'{rank}:\t{title}')
                datas.append({
                    "date": time.strftime("%Y-%m-%d", time.localtime()),
                    "rank": rank,
                    "title": escape_str(title),
                    "desc": escape_str(i['desc']),
                    "link": i['short_link_v2'],
                })
        else:
            for x, i in enumerate(self.obj["data"]["list"]):
                rank = x + 1
                title = i["title"]
                print(f'{rank}:\t{title}')
                datas.append({
                    "date": time.strftime("%Y-%m-%d", time.localtime()),
                    "rank": rank,
                    "title": escape_str(title),
                    "desc": escape_str(i['title']),
                    "link": f"https://www.bilibili.com/video/{i['bvid']}",
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
