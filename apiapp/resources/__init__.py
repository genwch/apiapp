from .auth import *
from .data import *
from .map import *


def init_routes(api):
    import gwcomm as comm
    apiroot = comm.sysconf.get("api_root", "/api/v1")
    api.add_resource(authapi, "/auth", endpoint="auth")
    api.add_resource(signapi, "/sign", endpoint="sign")
    urllst = [f"{apiroot}/data/<sec>/<model>",
              f"{apiroot}/data/<sec>/<model>/<id>", f"{apiroot}/data/<sec>/<model>/<col>/<id>"]
    apilst = []
    for i in range(len(urllst)):
        for s in [1, 2, 3]:
            api.add_resource(dataapi, urllst[i],
                             endpoint=f"data{s}_p{i}", resource_class_kwargs={"security": s})
        apilst.append({"endpoint": f"data<sec>_p{i}", "url": urllst[i]})
    api.add_resource(mapapi, apiroot, resource_class_args=(apilst),
                     resource_class_kwargs={"model_path": "./model"}, endpoint="map")
    api.add_resource(mapapi, f"{apiroot}/1", resource_class_args=(apilst),
                     resource_class_kwargs={"model_path": "./model/public"}, endpoint="map1")
    api.add_resource(mapapi, f"{apiroot}/2", resource_class_args=(apilst),
                     resource_class_kwargs={"model_path": "./model/protected"}, endpoint="map2")
    api.add_resource(mapapi, f"{apiroot}/3", resource_class_args=(apilst),
                     resource_class_kwargs={"model_path": "./model/private"}, endpoint="map3")
