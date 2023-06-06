from quart import Websocket, websocket
from gpgui.cbtools import cbm
import asyncio
import logging
from urllib.parse import urlparse, parse_qs


class PubSubServer:
    subscribers: dict[str, set[Websocket]] = {}
    topics: dict[str, bytes] = {}

    @classmethod
    async def publish(cls, topic: str, message: bytes | str):
        cls.topics[topic] = message
        for subscriber in PubSubServer.subscribers.get(topic, []):
            await subscriber.send(message)


@cbm.websocket("/pubsub")
async def socket_handler():
    # pylint: disable=protected-access
    this_ws: Websocket = websocket._get_current_object()  # type: ignore

    url_p = urlparse(this_ws.url)
    query = parse_qs(url_p.query, keep_blank_values=True)

    for sub in query.get("sub", []):
        PubSubServer.subscribers.setdefault(sub, set()).add(this_ws)
        if sub in PubSubServer.topics:
            await this_ws.send(PubSubServer.topics[sub])

    try:
        while True:
            mdata = await this_ws.receive()
            for topic_pub in query.get("pub", []):
                await PubSubServer.publish(topic_pub, mdata)

    except asyncio.CancelledError as e:
        msg = f"websocket cancelled {str(e)}"
        logging.info(msg)
        raise e

    except ValueError as value_error:
        await websocket.close(1003, reason=str(value_error))
        raise value_error

    finally:
        for subscribers in PubSubServer.subscribers.values():
            subscribers.discard(this_ws)
