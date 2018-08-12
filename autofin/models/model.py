from peewee import Model as PeeweeModel

from autofin.db import database


class Model(PeeweeModel):
    """Base model for database models."""

    class Meta:
        database = database
