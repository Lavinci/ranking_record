from core.webs import WebHots
from core.utils import parseJson
import requests
import time
from pymysql.converters import escape_str


class zhihu(WebHots):
    def __init__(self):
        WebHots.__init__(self)

    def getCtx(self):
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
        }
        url = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=50&desktop=true"
        res = requests.get(url, headers=header)
        if res.status_code != 200:
            if (res.status_code == 403):
                print("触发验证码")
                print(res.text)
            self.obj.clear()
            return
        self.obj = parseJson(res.text)
        if len(self.obj) == 0:
            return

    def parse(self):
        datas = list()
        for i in self.obj["data"]:
            rank = int(i["id"].split('_')[0])+1
            title = escape_str(i['target']['title'])
            print(f'{rank}:\t{title}')
            datas.append({
                "date": time.strftime("%Y-%m-%d", time.localtime()),
                "rank": rank,
                "title": title,
                "desc": escape_str(i['target']['excerpt']),
                "link": f'https://www.zhihu.com/question/{i["target"]["id"]}',
            })
        return datas

    def updateDB(self, res: list):
        name = "zhihu"
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
    hot = zhihu()
    hot.run()
