from flask_restful import Resource
from flask_jwt_extended import jwt_required
import gwcomm as comm

lg = comm.logger(__name__)


class authapi(Resource):
    def post(self):
        """Post Method - Login

        Request JSON:
            usr_cde {string} -- User Code
            password {string} -- Password

        Returns:
            dict -- {"access_token": {{Bearer token}}}
            int -- 200 - success, 401 - fail
        """
        lg.info("Post Method")
        from flask import request
        from flask_jwt_extended import create_access_token
        from flask_restplus import abort
        from lib.modlogin import modlogin
        import datetime
        body = request.get_json()
        if body == None:
            abort(401, msg="Invalid user or password")
        owner = body.get("usr_cde", None)
        owner = comm.sysconf.get(
            "srv_id", "SYSTEM") if owner == None else owner
        login = modlogin(owner=owner)
        chk, df = login.check(usr_cde=body.get(
            "usr_cde", None), password=body.get("password", None))
        del login
        if not(chk):
            abort(401, msg="Invalid user or password")
        exp = datetime.timedelta(hours=12)
        id = {k: v for k, v in df[0].items() if k in ["usr_cde", "acl"]}
        token = create_access_token(
            identity=id, expires_delta=exp)
        return {"access_token": token}, 200


class signapi(Resource):
    """API Resource - Registration

    Methods:
        POST -- Register
    """

    @jwt_required
    def post(self):
        """Post Method - Register

        Returns:
            dict -- Message
            int -- 200 - success, 401 - fail
        """
        from flask_restplus import abort
        from lib.token import decode_token
        from flask import request
        from lib.modlogin import modlogin
        token = request.headers.get("Authorization")
        identity, token = decode_token(token)
        acl = -1
        if identity.get("acl", 0) != acl:
            abort(401, msg=f"ACL not enough - required {acl}")
        body = request.get_json()
        owner = body.get("usr_cde", None)
        owner = comm.sysconf.get(
            "SRV_ID", "SYSTEM") if owner == None else owner
        login = modlogin(owner=owner)
        rtn = login.reg(body)
        del login
        if not(rtn):
            abort(401, msg="Registration fail")
        return {"msg": f"Registered. Welcome {owner}"}, 200
