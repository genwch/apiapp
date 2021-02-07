from flask_restful import Resource
import gwcomm as comm

lg = comm.logger(__name__)


class mapapi(Resource):
    def __init__(self, *args, **kwargs):
        self.__res = [a for a in args]
        self.__datas = self.__get_types(kwargs.get("data_path", ""))
        self.__scrapes = self.__get_types(kwargs.get("scrape_path", ""))
        self.__gimy = self.__get_types(kwargs.get("gimy_path", ""))

    def __get_types(self, path):
        import os
        fs = comm.filesystem()
        return [{"type": c.get("name")} for c in fs.ls_dict(os.path.join(path, "*.json"))]

    def get(self):
        lg.info("Get Method")
        rtn = {"endpoints": self.__res}
        if self.__datas != []:
            rtn["datas"] = self.__datas
        if self.__scrapes != []:
            rtn["scrapes"] = self.__scrapes
        if self.__gimy != []:
            rtn["gimy"] = self.__gimy
        return rtn, 200
