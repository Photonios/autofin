import structlog

from aiohttp import web

from autofin import settings

LOGGER = structlog.get_logger(__name__)


async def on_sms_received(request):
    """HTTP handler for the webhook that is called when
    a SMS is received."""
    data = await request.json()
    print(data)
    return web.Response(text="ok")


def twillio_webhook_server():
    """Starts a HTTP server to receive Twillio webhooks on."""

    app = web.Application()
    app.add_routes([web.view("/webhooks/twillio/sms", on_sms_received)])

    port = settings.TWILLIO_WEBHOOK_SERVER_PORT
    LOGGER.info("Twillio webhook server starting", port=port)
    web.run_app(app, port=int(port))


if __name__ == "__main__":
    twillio_webhook_server()
