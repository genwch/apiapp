from flask_restful import Resource
import gwcomm as comm

lg = comm.logger(__name__)


class mapapi(Resource):
    def __init__(self, *args, **kwargs):
        from flask_restful import url_for
        from glob import glob
        import os
        import re
        self.__res = [a for a in args]
        path = kwargs.get("model_path", [])
        self.__models = [{"type": re.sub(".json", "", re.sub(
            f"{path}/", "", f))} for f in glob(os.path.join(path, "*.json"))]

    def get(self):
        lg.info("Get Method")
        return {"endpoints": self.__res, "models": self.__models}, 200
