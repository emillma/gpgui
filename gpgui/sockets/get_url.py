from urllib.parse import urlparse
import quart
from gpgui import config


def get_pubsub_url(pub=None, sub=None, local=False):
    querys = []
    if pub:
        pub = [pub] if isinstance(pub, str) else pub
        querys.extend([f"pub={p}" for p in pub])
    if sub:
        sub = [sub] if isinstance(sub, str) else sub
        querys.extend([f"sub={s}" for s in sub])
    query = "&".join(querys)
    url = (
        quart.request.host_url
        if quart.has_request_context() and not local
        else f"http://127.0.0.1:{config.PORT}/"
    )
    return urlparse(url)._replace(scheme="ws", path="/pubsub", query=query).geturl()
