from flask import Blueprint
import gwcomm as comm

fs = comm.filesystem()
fname = fs.fname(__file__)
static = Blueprint(fname, __name__)
lg = comm.logger(__name__)


@static.route("/link/<media>/<st>/<ep>")
def getlink(*args, **kwargs):
    import gwws as ws
    import resources as res
    from flask import redirect
    media = kwargs.get("media", None)
    st = kwargs.get("st", None)
    ep = kwargs.get("ep", None)
    lg.debug(f"media: {media} st: {st}, ep: {ep}")
    gimy = res.gimyscrape(scrape_path="./conf/scrape/gimy.tv")
    linkws = ws.gimy_scrape(conf=gimy.conf)
    if st == None or ep == None:
        return "", 404
    lst = [{"st": st, "ep": ep}]
    data = linkws.get(type="links", lst=[
        {"media_id": media, "stream_ep": lst}])
    if data == []:
        return "", 404
    for d in data:
        url = d.get("url")
        break
    return redirect(url)


# @static.route("/link/<media>/e/<ep>")
# @static.route("/link/<media>/s/<st>")
# @static.route("/link/<media>/<st>/<ep>")
# def getlink(*args, **kwargs):
#     import gwws as ws
#     import resources as res
#     from flask import redirect, Response
#     import re
#     import requests
#     media = kwargs.get("media", None)
#     st = kwargs.get("st", None)
#     ep = kwargs.get("ep", None)
#     lg.debug(f"media: {media} st: {st}, ep: {ep}")
#     gimy = res.gimyscrape(scrape_path="./conf/scrape/gimy.tv")
#     streamws = ws.gimy_scrape(conf=gimy.conf)
#     linkws = ws.gimy_scrape(conf=gimy.conf)
#     if st != None and ep != None:
#         eplst = [{"st": st, "ep": ep}]
#     else:
#         stream = streamws.get(type="streams", lst=[{"media_id": media}])
#         t = []
#         for s in stream:
#             t = s.get("stream_ep", [])
#             break
#         if st == None:
#             st = []
#             for s in t:
#                 s.update({"media_id": media})
#                 st.append(s)
#             eplst = [{"st": s.get("st", 1), "ep": s.get("ep", 1)}
#                      for s in st if s.get("ep", 1) == ep]
#         elif ep == None:
#             ep = []
#             for s in t:
#                 s.update({"media_id": media})
#                 ep.append(s)
#             eplst = [{"st": s.get("st", 1), "ep": s.get("ep", 1)}
#                      for s in ep if s.get("st", 1) == st if int(s.get("ep", 1)) <= 2]
#     data = linkws.get(type="links", lst=[
#         {"media_id": media, "stream_ep": eplst}])
#     # rtn = ["#EXTM3U", ]
#     rtn = ["#EXTM3U", "#EXT-X-START:TIME-OFFSET=0"]
#     cnt = 0
#     for d in data:
#         url = d.get("url")
#         rurl = "/".join(url.split("/")[:-1])
#         lg.info(f"rurl: {rurl}, url: {url}")
#         r = requests.get(url)
#         try:
#             lnk = str(r.content)
#             lnk = re.sub("^b'", "", lnk)
#             lnk = re.sub("'$", "", lnk)
#             lg.debug(f"lnk: {lnk}")
#             lnk = lnk.split("\\n")
#         except:
#             lnk = []
#         for l in lnk:
#             t = re.findall("^#EXTM3U", l)
#             if t == []:
#                 t = re.findall("^#EXT", l)
#                 if t == []:
#                     rtn.append(f"#EXT-X-MEDIA-SEQUENCE:{cnt}")
#                     cnt += 1
#                     rtn.append(f"#EXTINF:{cnt},{cnt}")
#                     l = f"{rurl}/{l}"
#                 # else:
#                 #     attr = l.split(":")[1].split(",")
#                     # attrs = {a.split("=")[0]: a.split("=")[1] for a in attr}
#                     # lg.debug(f"attrs: {attrs}")
#                     # attrs["PROGRAM-ID"] = cnt
#                     # l = "{}{}".format(
#                     #     "#EXT-X-STREAM-INF:", ",".join([f"{k}={v}" for k, v in attrs.items()]))
#                     rtn.append(l)
#     rtn.append("#EXT-X-ENDLIST")
#     rtn = "\n".join(rtn)
#     lg.debug(f"rtn: {rtn}")
#     return Response(rtn, mimetype='application/vnd.apple.mpegurl'), 200
    # return redirect(url)
