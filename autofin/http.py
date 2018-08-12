import requests


def create_session():
    """Creates a new HTTP session, all requests made within
    the session save their cookies as part of the session."""

    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36"
        }
    )

    return session
