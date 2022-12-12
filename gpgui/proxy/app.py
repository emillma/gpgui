import asyncio
from urllib.parse import urlparse
from quart import Quart, request, Response, redirect
from quart.helpers import stream_with_context
from aiohttp import hdrs
import aiohttp
import logging

app = Quart(__name__)
client: aiohttp.ClientSession
connector = aiohttp.TCPConnector(limit=8)


@app.before_serving
async def get_client():
    global client  # pylint: disable=global-statement
    client = aiohttp.ClientSession()


@app.route("/", defaults={"path": ""}, methods=list(hdrs.METH_ALL))
@app.route("/<path:path>", methods=list(hdrs.METH_ALL))
async def get(**_):
    url = urlparse(request.url)
    url_str = url._replace(netloc=f"{url.hostname}:8050").geturl()

    if request.method not in {"GET", "POST"}:
        logging.warning("Redirecting %s to %s", request.method, url_str)
        return redirect(url_str)

    req = await client.request(
        request.method,
        url_str,
        params=request.args,
        headers=request.headers,
        allow_redirects=False,
        data=await request.data,
    )
    response = await req.__aenter__()  # pylint: disable=unnecessary-dunder-call

    @stream_with_context
    async def async_generator():
        async for chunk in response.content.iter_chunked(2048):
            yield chunk
        await req.__aexit__(None, None, None)

    return async_generator(), response.status, dict(response.headers.items())


def run():
    app.run(debug=False, port=5000, use_reloader=False)


if __name__ == "__main__":
    app.run()
