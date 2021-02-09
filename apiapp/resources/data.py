from flask_restful import Resource
from flask_jwt_extended import jwt_required
import gwcomm as comm
from lib.token import *
from lib.paging import *

lg = comm.logger(__name__)


class dataapi(Resource):
    def __init__(self, *args, **kwargs):
        self.__reqacl = 0
        self.__acl = 0
        self.__owner = None
        self.__confpath = kwargs.get("conf_path", "./conf/data")
        self.__conf = {}

    def __parameters(self, para):
        from flask_restplus import abort
        import gwpd as pdfx
        model = para.get("type", None)
        sec = para.get("sec", 0)
        col = para.get("col", None)
        id = para.get("id", None)
        page = para.get("page", 1)
        self.__conf = comm.load_conf(
            "{}/{}.json".format(self.__confpath, model))
        if isinstance(sec, str):
            sec = int(sec)
        if model == None:
            abort(400, msg=f"Undefined <type>- {model}")
        lg.debug(f"set pd")
        try:
            dt = pdfx.pdvw(model=model, path=self.__confpath,
                           security=sec, owner=self.__owner)
        except Exception as e:
            lg.warning(f"{model} - Not view - {e}")
            try:
                lg.debug(f"{model} - start pdtb")
                dt = pdfx.pdtb(model=model, path=self.__confpath,
                               security=sec, owner=self.__owner)
                lg.debug(f"{model} - end pddt")
            except Exception as e:
                lg.warning(f"{model} - Not table - {e}")
                abort(
                    400, msg=f"{model} - Invalid <sec>/<model> - {sec}/{model}")

        if col == None:
            data = dt.get() if id == None else dt.get(key=id)
        else:
            data = dt.get(filter={col: id})
        try:
            acl = int(dt.acl) if isinstance(dt.acl, str) else dt.acl
        except:
            acl = 0
        return data, dt, acl, page

    @jwt_required
    def get(self, *args, **kwargs):
        lg.info("Get Method")
        from flask import request
        from flask_restplus import abort
        self.__owner, self.__acl = get_identity(request=request)
        data, obj, self.__reqacl, page = self.__parameters(kwargs)
        cols = {c.get("name"): c.get("model", "str") for c in obj._cols()}
        check_acl(self.__acl, self.__reqacl)
        if data == []:
            abort(404, msg="Not found", data=[], cols=cols, pages=1)
        paging = self.__conf.get("paging", 100)
        pages = 1
        if page != "all":
            try:
                page = int(page)
            except:
                page = 1
            data, pages = data_paging(data, paging, page)
        return {"data": data, "cols": cols, "pages": pages}, 200

    @jwt_required
    def post(self, *args, **kwargs):
        lg.info("Post Method")
        from flask import request
        from flask_restplus import abort
        self.__owner, self.__acl = get_identity(request=request)
        data, obj, self.__reqacl, _ = self.__parameters(kwargs)
        check_acl(self.__acl, self.__reqacl)

        # upsert
        from flask import request
        try:
            body = request.get_json()
        except:
            abort(400, msg="Invalid JSON")
        datas = body.get("datas", [])
        if datas == []:
            datas = [body]
        for d in datas():
            rtn, df = obj.upsert(d)
            if not(rtn):
                abort(400, msg="Upsert fail")
        rtn, _ = obj.save()
        if not(rtn):
            abort(400, msg="Save fail")
        lg.debug(df)
        return {"data": obj.get()}, 200
