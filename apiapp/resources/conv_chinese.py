from flask_restful import Resource
from flask_jwt_extended import jwt_required
import gwcomm as comm
from lib.token import *
from pyhanlp import *

lg = comm.logger(__name__)


class conv_chinapi(Resource):
    def __init__(self, *args, **kwargs):
        self.__reqacl = 0
        self.__acl = 0
        self.__owner = None

    def __parameters(self, para):
        from flask_restplus import abort
        import gwpd as pdfx
        to = para.get("to", None)
        return to

    @jwt_required
    def get(self, *args, **kwargs):
        lg.info("Get Method")
        from flask import request
        from flask_restplus import abort
        self.__owner, self.__acl = get_identity(request=request)
        js = request.get_json()
        data = js.get("data", "")
        to = self.__parameters(kwargs)
        check_acl(self.__acl, self.__reqacl)
        if data == "":
            abort(404, msg="Not found")
        if to == "tc":
            data = HanLP.convertToTraditionalChinese(data)
        elif to == "sc":
            data = HanLP.convertToSimplifiedChinese(data)
        return {"data": data}, 200
