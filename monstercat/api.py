import requests

from . import settings

BASE_URL = "https://player.monstercat.app/api"

# Configure session object w/ cookie
_session = requests.session()
if "cookie" in settings.config:
    _cookies = requests.cookies.cookiejar_from_dict(settings.config["cookie"])
    _session.cookies = _cookies


def login(email, password):
    r = _session.post(
        f"{BASE_URL}/sign-in", json={"email": email, "password": password}
    )
    r.raise_for_status()
    return r


def logout():
    r = _session.post(f"{BASE_URL}/sign-out")
    r.raise_for_status()
    return r


def session():
    r = _session.get(f"{BASE_URL}/me")
    r.raise_for_status()
    return r.json()


def releases(**kwargs):
    r = _session.get(f"{BASE_URL}/releases", params=kwargs)
    r.raise_for_status()
    return r.json()


def generate_release_link(release_id, file_format):
    return f"{BASE_URL}/release/{release_id}/download?format={file_format}"


def download_file(url, outfile, callback=None):
    with _session.get(url, stream=True) as r:
        r.raise_for_status()
        content_len = int(r.headers.get('content-length'))
        done = 0
        with open(outfile, "wb") as fid:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    fid.write(chunk)
                    done += len(chunk)
                    if callback:
                        callback(done / content_len)
