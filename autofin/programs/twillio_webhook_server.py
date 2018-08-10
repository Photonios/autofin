import structlog

from aiohttp import web
from urllib.parse import unquote

from autofin import settings
from autofin.error import capture_error, capture_error_context
from autofin.billing import InvoiceManager
from autofin.messaging import MessageFormatter

LOGGER = structlog.get_logger(__name__)


async def on_sms_received(request):
    """HTTP handler for the webhook that is called when
    a SMS is received."""

    try:
        context = dict(raw_body=await request.text())
        capture_error_context(**context)
        logger = LOGGER.bind(**context)

        data = await request.post()

        from_ = data.get("From")
        if not from_:
            logger.error("Received bad request, missing from")
            return web.Response(status=400, text="Missing 'From'")

        body = data.get("Body")
        if not body:
            logger.error("Received bad request, missing body")
            return web.Response(status=400, text="Missing 'Body'")

        context["message"] = body
        context["phone_number"] = from_
        logger = logger.bind(**context)
        capture_error_context(**context)

        logger.debug("Received SMS")

        command = body.lower().replace(" ", "")
        if command == "getbills":
            logger.info("Received command through SMS", command=command)
        else:
            logger.error("Receive unknown command through SMS", command=command)
            return web.Response(text=MessageFormatter.unknown_command(command))

        invoices = InvoiceManager().get_latest_invoices()
        return web.Response(text=MessageFormatter.invoices(invoices))
    except Exception:
        error_id = capture_error()
        return web.Response(text=MessageFormatter.error(error_id))


def twillio_webhook_server():
    """Starts a HTTP server to receive Twillio webhooks on."""

    app = web.Application()
    app.add_routes([web.post("/webhooks/twillio/sms", on_sms_received)])

    port = settings.TWILLIO_WEBHOOK_SERVER_PORT
    LOGGER.info("Twillio webhook server starting", port=port)
    web.run_app(app, port=int(port), print=None)


if __name__ == "__main__":
    twillio_webhook_server()
