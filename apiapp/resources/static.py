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
    data = linkws.get(type="links", lst=[
                      {"media_id": media, "stream_ep": [{"st": st, "ep": ep}]}])
    url = data[0].get("url")
    return redirect(url)
