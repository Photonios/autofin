import sys
import traceback
import structlog

from raven import Client

from autofin import settings

__raven__ = None
LOGGER = structlog.get_logger(__name__)


if settings.SENTRY_DSN:
    __raven__ = Client(
        settings.SENTRY_DSN,
        environment=settings.SENTRY_ENVIRONMENT,
        auto_log_stacks=True,
    )

    LOGGER.info("Sentry enabled", env=settings.SENTRY_ENVIRONMENT)


def capture_error() -> str:
    """Captures the current exception and sends it to Sentry."""

    if __raven__:
        return __raven__.captureException()

    traceback.print_exc()
    return "LOCAL_ERROR"


def capture_error_context(**values) -> None:
    """Adds context to the next error that is going to be captured."""

    if __raven__:
        __raven__.user_context(values)
