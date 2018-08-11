from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from autofin import settings


def create_browser():
    """Creates a new Selenium "browser"

    This utility function exists so we can apply some
    app wide settings related to the browser."""

    chrome_options = Options()
    chrome_options.add_argument("--blink-settings=imagesEnabled=false")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--start-maximized")

    if settings.SELENIUM_HEADLESS_ENABLED:
        chrome_options.add_argument("--headless")

    browser_options = dict(chrome_options=chrome_options)
    if settings.SELENIUM_CHROME_DRIVER_PATH:
        browser_options["executable_path"] = settings.SELENIUM_CHROME_DRIVER_PATH

    browser = webdriver.Chrome(**browser_options)
    return browser
