import os
import structlog

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from autofin import settings

LOGGER = structlog.get_logger(__name__)


def create_browser(name: str):
    """Creates a new Selenium "browser"

    This utility function exists so we can apply some
    app wide settings related to the browser."""

    profile_path = os.path.join(settings.SELENIUM_CHROME_PROFILE_PATH, name)

    chrome_options = Options()
    chrome_options.add_argument("--blink-settings=imagesEnabled=false")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--user-data-dir=%s" % profile_path)

    if settings.SELENIUM_HEADLESS_ENABLED:
        chrome_options.add_argument("--headless")

    LOGGER.info("Launching chrome", args=chrome_options.arguments)

    browser_options = dict(chrome_options=chrome_options)
    if settings.SELENIUM_CHROME_DRIVER_PATH:
        browser_options["executable_path"] = settings.SELENIUM_CHROME_DRIVER_PATH

    browser = webdriver.Chrome(**browser_options)
    return browser
