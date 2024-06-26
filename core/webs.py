from abc import ABCMeta, abstractmethod
import core.mysql as mysql


class WebHots(metaclass=ABCMeta):
    def __init__(self):
        self.obj = {}
        self.db = mysql.DB("docker_mysql", 'root', '123456')

    @abstractmethod
    def getCtx(self):
        pass

    @abstractmethod
    def parse(self):
        pass

    @abstractmethod
    def getCtxSuccess(self):
        pass

    def getCtxSuccess(self):
        return len(self.obj) > 0

    @abstractmethod
    def updateDB(self, res: list):
        pass

    def run(self):
        self.getCtx()
        if not self.getCtxSuccess():
            print("run error, please check.")
            return
        res = self.parse()
        self.updateDB(res)
