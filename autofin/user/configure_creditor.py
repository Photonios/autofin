import structlog

from autofin import models
from autofin.billing.creditors import CreditorID

LOGGER = structlog.get_logger(__name__)


def configure_creditor(
    user: models.Creditor,
    creditor_id: CreditorID,
    username: str,
    password: str,
    enabled: bool = True,
) -> None:
    """Configures a creditor for the specified user."""

    (
        models.UserCreditorConfig.insert(
            user=user,
            creditor_id=creditor_id,
            username=username,
            password=password,
            enabled=enabled,
        ).execute()
    )

    LOGGER.info(
        "Configured creditor for user",
        user=user,
        creditor_id=creditor_id,
        username=username,
        enabled=enabled,
    )
