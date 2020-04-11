import requests

from . import settings

BASE_URL = "https://connect.monstercat.com/v2"

SELF = f"{BASE_URL}/self"
SESSION = f"{SELF}/session"
SIGN_IN = f"{BASE_URL}/signin"
SIGN_OUT = f"{BASE_URL}/signout"

# Configure session object w/ cookie
_session = requests.session()
if "cookie" in settings.config:
    _cookies = requests.cookies.cookiejar_from_dict(settings.config["cookie"])
    _session.cookies = _cookies


def login(email, password):
    r = _session.post(SIGN_IN, json={"email": email, "password": password})
    r.raise_for_status()
    return r


def logout():
    r = _session.post(SIGN_OUT)
    r.raise_for_status()
    return r


def session():
    r = _session.get(SESSION)
    r.raise_for_status()
    return r.json()
