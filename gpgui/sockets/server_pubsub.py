from quart import Websocket, websocket
from gpgui.cbtools import cbm
import asyncio
import logging
from urllib.parse import urlparse, parse_qs


class SocketServerPubSub:
    topics: dict[str, set[Websocket]] = {}


@cbm.websocket("/pubsub")
async def socket_handler():
    # pylint: disable=protected-access
    this_ws: Websocket = websocket._get_current_object()  # type: ignore

    url_p = urlparse(this_ws.url)
    query = parse_qs(url_p.query, keep_blank_values=True)

    for sub in query.get("sub", []):
        SocketServerPubSub.topics.setdefault(sub, set()).add(this_ws)

    try:
        while True:
            mdata = await this_ws.receive()
            for pub in query.get("pub", []):
                for subscriber in SocketServerPubSub.topics.get(pub, []):
                    await subscriber.send(mdata)

    except asyncio.CancelledError as e:
        msg = f"websocket cancelled {str(e)}"
        logging.info(msg)
        raise e

    except ValueError as value_error:
        await websocket.close(1003, reason=str(value_error))
        raise value_error

    finally:
        for subscribers in SocketServerPubSub.topics.values():
            subscribers.discard(this_ws)
