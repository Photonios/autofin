import os

from peewee import SqliteDatabase

from autofin import settings

database = SqliteDatabase(os.path.join(settings.STORAGE_PATH, "autofin.db"))
