from flask_restful import Resource
from flask_jwt_extended import jwt_required
import gwcomm as comm
from lib.token import *

lg = comm.logger(__name__)


class dataapi(Resource):
    def __init__(self, *args, **kwargs):
        self.__reqacl = 0
        self.__acl = 0
        self.__owner = None

    # def __get_identity(self, request):
    #     from lib.token import decode_token
    #     from flask_restplus import abort
    #     token = request.headers.get("Authorization")
    #     identity, _ = decode_token(token=token)
    #     self.__owner = identity.get("usr_cde", None)
    #     self.__acl = identity.get("acl", 0)
    #     if isinstance(self.__acl, str):
    #         self.__acl = int(self.__acl)
    #     return self.__owner, self.__acl

    # def __check_acl(self):
    #     from flask_restplus import abort
    #     if self.__acl < self.__reqacl:
    #         abort(401, msg="ACL not enough - required {}".format(self.__reqacl))
    #         return False
    #     return True

    def __parameters(self, para):
        from flask_restplus import abort
        import gwpd as pdfx
        model = para.get("model", None)
        sec = para.get("sec", 0)
        col = para.get("col", None)
        id = para.get("id", None)
        if isinstance(sec, str):
            sec = int(sec)
        if model == None:
            abort(400, msg=f"Undefined <model>- {model}")
        lg.debug(f"set pd")
        try:
            dt = pdfx.pdvw(model=model, security=sec, owner=self.__owner)
        except Exception as e:
            lg.warning(f"{model} - Not view - {e}")
            try:
                lg.debug(f"{model} - start pdtb")
                dt = pdfx.pdtb(model=model, security=sec, owner=self.__owner)
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
        return data, dt, acl

    @jwt_required
    def get(self, *args, **kwargs):
        lg.info("Get Method")
        from flask import request
        from flask_restplus import abort
        self.__owner, self.__acl = get_identity(request=request)
        data, obj, self.__reqacl = self.__parameters(kwargs)
        cols = {c.get("name"): c.get("model", "str") for c in obj._cols()}
        check_acl(self.__acl, self.__reqacl)
        if data == []:
            abort(404, msg="Not found", data=[], cols=cols)
        return {"data": data, "cols": cols}, 200

    @jwt_required
    def post(self, *args, **kwargs):
        lg.info("Post Method")
        from flask import request
        from flask_restplus import abort
        self.__owner, self.__acl = get_identity(request=request)
        data, obj, self.__reqacl = self.__parameters(kwargs)
        check_acl(self.__acl, self.__reqacl)

        # upsert
        from flask import request
        try:
            body = request.get_json()
        except:
            abort(400, msg="Invalid JSON")

        rtn, df = obj.upsert(body)
        if not(rtn):
            abort(400, msg="Upsert fail")
        rtn, _ = obj.save()
        if not(rtn):
            abort(400, msg="Save fail")
        lg.debug(df)
        return {"data": obj.get()}, 200
