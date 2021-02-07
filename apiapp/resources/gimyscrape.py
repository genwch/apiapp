from flask_restful import Resource
from flask_jwt_extended import jwt_required
import gwcomm as comm
import gwws as ws
from lib.token import *
from .scrape import *

lg = comm.logger(__name__)


class gimyscrape(scrapeapi):
    def parameters(self, para):
        type = para.get("type", None)
        id = para.get("id", None)
        st = para.get("st", None)
        ep = para.get("ep", None)
        if id != None and type != None:
            if type == "cat":
                lst = {}
            elif type == "subcat":
                lst = {"cat_id": id}
            elif type == "media":
                lst = {"scat_id": id}
            elif type == "stream":
                # lst = {"scat_id": id}
                lst = {"media_id": id}
            elif type == "link":
                lst = {"media_id": id}
                if st != None and ep != None:
                    stream_ep = {}
                    stream_ep["st"] = st
                    stream_ep["ep"] = ep
                    lst["stream_ep"] = [stream_ep]
        else:
            lst = {}
        type = f"{type}s" if type != None else None
        return type, [lst]

    @jwt_required
    def get(self, *args, **kwargs):
        lg.info("Get Method")
        from flask import request
        from flask_restplus import abort
        self.__owner, self.__acl = get_identity(request=request)
        js = request.get_json()
        type, lst = self.parameters(kwargs)
        conf = js if js != None else self.conf
        if conf == None or conf == {}:
            abort(404, msg="Config not defined")
        if type == None:
            abort(404, msg="type not defined")
        check_acl(self.__acl, self.reqacl)
        # lg.debug(f"conf: {conf}")
        dataws = ws.gimy_scrape(conf=conf)
        u = conf.get("stream", {}).get("url", "")
        lg.debug(f"type: {type}, lst: {lst}, url: {u}")
        data = dataws.get(type=type, lst=lst)
        return {"data": data}, 200
