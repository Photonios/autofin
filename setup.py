import os
import subprocess
import distutils.cmd

from setuptools import find_packages, setup


class BaseCommand(distutils.cmd.Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass


def create_command(text, cmd):
    """Creates a custom setup.py command."""

    class CustomCommand(BaseCommand):
        description = text

        def run(self):
            subprocess.check_call(cmd)

    return CustomCommand


class MigrateCommand(BaseCommand):
    description = "Migrates the database"

    def run(self):
        from autofin import models
        from autofin.db import database
        from autofin.billing.creditors import CreditorID

        database.create_tables(
            [
                models.Creditor,
                models.User,
                models.Invoice,
                models.UserCreditorConfig,
                models.UserContactMethod,
            ]
        )

        for creditor_id in CreditorID.all():
            name = CreditorID.human_readable(creditor_id)
            models.Creditor.replace(id=creditor_id, name=name).execute()


with open(
    os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf-8"
) as readme:
    README = readme.read()

setup(
    name="autofin",
    version="1.0",
    packages=find_packages(),
    include_package_data=True,
    license="MIT License",
    description="Automatically track finance related things.",
    long_description=README,
    url="https://github.com/Photonios/autofin",
    author="Swen Kooij",
    author_email="swenkooij@gmail.com",
    keywords=["autofin", "swen", "kooij", "finance", "track"],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    cmdclass={
        "format": create_command("Formats the code", ["black", "autofin", "setup.py"]),
        "migrate": MigrateCommand,
    },
)
