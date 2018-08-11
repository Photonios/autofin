import os
import shutil
import structlog
import sqlite3
import functools

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from autofin import settings, storage

LOGGER = structlog.get_logger(__name__)


class BrowserManager:
    """Helps managing browsers, it configures them according
    to the settings and does some hacky hacky."""

    def __init__(self, session_name: str) -> None:
        """Initializes a new instance of :see:BrowserManager.

        Arguments:
            session_name:
                The name of the session the browser manager
                should use. If the same name is used in-between
                runs, then the cache and cookies are kept.
        """

        self.session_name = session_name
        self.cleaned_session_name = self.session_name.replace(" ", "").lower()

        self.profile_path = os.path.join(
            settings.SELENIUM_CHROME_PROFILE_PATH, self.cleaned_session_name
        )

        self._browser = None

    def create_browser(self):
        """Creates a new browser instance."""

        chrome_options = Options()
        chrome_options.add_argument("--blink-settings=imagesEnabled=false")
        chrome_options.add_argument("--window-size=1000,800")
        chrome_options.add_argument("--user-data-dir=%s" % self.profile_path)

        if settings.SELENIUM_HEADLESS_ENABLED:
            chrome_options.add_argument("--headless")

        LOGGER.info("Launching chrome", args=chrome_options.arguments)

        browser_options = dict(chrome_options=chrome_options)
        if settings.SELENIUM_CHROME_DRIVER_PATH:
            browser_options["executable_path"] = settings.SELENIUM_CHROME_DRIVER_PATH

        self._browser = webdriver.Chrome(**browser_options)
        return self._browser

    def destroy_browser(self):
        """Destroys the current browser instance.

        Patches session cookies to be non-session cookies,
        set to expire in 2099. This allows us to stay
        logged in on website which use session cookies."""
        if self._browser:
            self._browser.close()

        cookies_db_path = os.path.join(self.profile_path, "Default/Cookies")

        cookies_db = sqlite3.connect(cookies_db_path)
        cookies_db.execute(
            "update cookies set expires_utc = 41023584000000000, has_expires = 1, is_persistent = 1 where expires_utc = 0"
        )
        cookies_db.commit()
        cookies_db.close()
