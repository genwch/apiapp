from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
import gwcomm as comm
import resources as res

lg = comm.logger(__name__)
lg.info("init")
app = Flask(__name__)
api = Api(app)
comm.add_env(["SECRET_KEY", "SRV_ID", "SRV_SCT", "API_ROOT"])
app.config["SECRET_KEY"] = comm.sysconf.get("secret_key")
jwt = JWTManager(app)
res.init_routes(api)
