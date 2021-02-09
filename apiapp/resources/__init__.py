from .auth import *
from .data import *
from .map import *
from .convc import *
from .scrape import *
from .gimyscrape import *


def init_routes(api):
    import gwcomm as comm
    apiroot = comm.sysconf.get("api_root", "/api/v1")
    apilst = []

    # auth
    api.add_resource(authapi, "/auth", endpoint="auth")
    api.add_resource(signapi, "/sign", endpoint="sign")

    # data
    urllst = [f"{apiroot}/data/<sec>/<type>", f"{apiroot}/data/<sec>/<type>/p/<page>",
              f"{apiroot}/data/<sec>/<type>/<id>", f"{apiroot}/data/<sec>/<type>/<id>/p/<page>",
              f"{apiroot}/data/<sec>/<type>/<col>/<id>", f"{apiroot}/data/<sec>/<type>/<col>/<id>/p/<page>"]
    datalst = []
    seclst = [1, 2, 3, 9]
    secpath = ["public", "protected", "private", "auth"]
    for i in range(len(urllst)):
        for s in seclst:
            api.add_resource(dataapi, urllst[i],
                             endpoint=f"data{s}_p{i}", resource_class_kwargs={"data_path": "./conf/data", "security": s})
        datalst.append({"endpoint": f"data<sec>_p{i}", "url": urllst[i]})
    apilst += datalst

    # conv
    api.add_resource(
        convcapi, f"{apiroot}/convc/<to>", endpoint="convert_chinese")
    apilst.append({"endpoint": "convert_chinese",
                   "url": f"{apiroot}/convc/<sc|tc>"})

    # scrape
    urllst = [f"{apiroot}/scrape", f"{apiroot}/scrape/<type>",
              f"{apiroot}/scrape/<type>/p/<page>"]
    scrapelst = []
    for i in range(len(urllst)):
        api.add_resource(
            scrapeapi, urllst[i], resource_class_kwargs={"scrape_path": "./conf/scrape"}, endpoint=f"scrape_p{i}")
        scrapelst.append({"endpoint": f"scrape_p{i}", "url": urllst[i]})
    apilst += scrapelst

    # gimy scrape
    urllst = [f"{apiroot}/gimy/<type>", f"{apiroot}/gimy/<type>/p/<page>",
              f"{apiroot}/gimy/<type>/<id>", f"{apiroot}/gimy/<type>/<id>/p/<page>",
              f"{apiroot}/gimy/<type>/scat_id/<scat_id>", f"{apiroot}/gimy/<type>/scat_id/<scat_id>/p/<page>",
              f"{apiroot}/gimy/<type>/<id>/<st>/<ep>", f"{apiroot}/gimy/<type>/<id>/<st>/<ep>/p/<page>"]
    gimylst = []
    for i in range(len(urllst)):
        api.add_resource(
            gimyscrape, urllst[i], resource_class_kwargs={"scrape_path": "./conf/scrape/gimy.tv"}, endpoint=f"gimy_p{i}")
        gimylst.append({"endpoint": f"gimy_p{i}", "url": urllst[i]})
    apilst += gimylst

    # map
    api.add_resource(mapapi, f"{apiroot}", resource_class_args=(apilst),
                     resource_class_kwargs={"data_path": "./conf/data", "scrape_path": "./conf/scrape", "gimy_path": "./conf/scrape/gimy.tv"}, endpoint="map")
    api.add_resource(mapapi, f"{apiroot}/data", resource_class_args=(datalst),
                     resource_class_kwargs={"data_path": "./conf/data"}, endpoint="map_data")
    api.add_resource(mapapi, f"{apiroot}/gimy", resource_class_args=(gimylst),
                     resource_class_kwargs={"gimy_path": "./conf/scrape/gimy.tv"}, endpoint="map_gimy")
    for s in range(len(seclst)):
        api.add_resource(mapapi, f"{apiroot}/data/{seclst[s]}", resource_class_args=(datalst),
                         resource_class_kwargs={"data_path": f"./conf/data/{secpath[s]}"}, endpoint=f"map_data_s{seclst[s]}")
    # for s in range(len(scrapelst)):
    #     api.add_resource(mapapi, scrapelst[s], resource_class_args=(scrapelst), endpoint=f"map_scrape_{s}")
