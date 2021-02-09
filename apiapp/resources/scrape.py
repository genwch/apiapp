from flask_restful import Resource
from flask_jwt_extended import jwt_required
import gwcomm as comm
import gwws as ws
from lib.token import *
from lib.paging import *

lg = comm.logger(__name__)


class scrapeapi(Resource):
    def __init__(self, *args, **kwargs):
        self.reqacl = 0
        self.__acl = 0
        self.__owner = None
        path = kwargs.get("scrape_path", "")
        self.__read_cfg(path)
        self.conf = comm.sysconf.get("scrape", {})

    def __read_cfg(self, path):
        import os
        fs = comm.filesystem()
        cfg = {}
        for c in fs.ls_dict(os.path.join(path, "*.json")):
            cfg[c.get("name")] = comm.load_conf(c.get("full"))
        comm.sysconf["scrape"] = cfg

    def parameters(self, para):
        type = para.get("type", None)
        page = para.get("page", 1)
        return type, page

    @jwt_required
    def get(self, *args, **kwargs):
        lg.info("Get Method")
        from flask import request
        from flask_restplus import abort
        self.__owner, self.__acl = get_identity(request=request)
        js = request.get_json()
        type, page = self.parameters(kwargs)
        conf = js if js != None else self.conf
        if conf == None or conf == {}:
            abort(404, msg="Config not defined")
        if type == None:
            conf = {"data": conf}
            type = "data"
        check_acl(self.__acl, self.reqacl)
        dataws = ws.scrape(name=type, conf=conf)
        data = dataws.items()
        if conf.get(type, {}).get("info", {}) == {}:
            return {"content": str(dataws.content())}, 200
        else:
            paging = self.conf.get("paging", 100)
            pages = 1
            if page != "all":
                try:
                    page = int(page)
                except:
                    page = 1
                data, pages = data_paging(data, paging, page)
            return {"data": data, "pages": pages}, 200
