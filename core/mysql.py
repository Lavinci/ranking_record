import pymysql

class DB:
    def __init__(self, ip: str, user: str, password: str, port=3306, charset='utf8mb4'):
        self.ip = ip
        self.user = user
        self.password = password
        self.port = port
        self.charset = charset
        self.conn = None

    def __del__(self):
        if self.conn is not None:
            self.conn.close()

    def connect(self, db_name: str):
        self.conn = pymysql.connect(host=self.ip, port=self.port, user=self.user, password=self.password,
                                    charset=self.charset)
        # print(self.conn.get_server_info())
        self.conn.select_db(db_name)

    def disconnect(self):
        self.conn.close()

    def exec(self, cmd: str):
        # print(f"exec cmd {cmd.strip()}")
        cursor = self.conn.cursor()
        cursor.execute(cmd)
        self.conn.commit()
        res = cursor.fetchall()
        cursor.close()
        return res


if __name__ == '__main__':
    db = DB('192.168.8.233', 'root', '123456')
    db.connect('hot')
    res = db.exec("select * from zhihu")
    print(res)
