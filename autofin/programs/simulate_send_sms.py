import argparse
import structlog
import requests

from autofin import settings

LOGGER = structlog.get_logger(__name__)


def simulate_send_sms(from_: str, body: str) -> None:
    """Simulates sending a SMS message by calling the Twillio
    WebHook endpoint directly."""

    url = (
        "http://localhost:%d/webhooks/twillio/sms"
        % settings.TWILLIO_WEBHOOK_SERVER_PORT
    )
    data = dict(From=from_, Body=body)

    LOGGER.info("Simulating Twillio Webhook call", url=url, data=data)
    response = requests.post(url, data)

    LOGGER.info("Received a message back", message=response.text)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simulates sending an SMS.")

    parser.add_argument("--from", dest="from_", action="store", default="+40773818041")
    parser.add_argument("--body", dest="body", action="store", default="GETBILLS")

    args = parser.parse_args()
    simulate_send_sms(args.from_, args.body)
