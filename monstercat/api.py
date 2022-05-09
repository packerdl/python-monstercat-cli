import requests

from . import settings
from .models import Release, Track, User

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


def me():
    r = _session.get(f"{BASE_URL}/me")
    r.raise_for_status()
    # If not logged in, the sign in page is returned with 200 status
    if r.status_code == 200 and r.headers["Content-Type"] == "text/html":
        raise requests.HTTPError("Not signed in", response=r)
    return User().load(r.json()["User"])


def releases(**kwargs):
    r = _session.get(f"{BASE_URL}/releases", params=kwargs)
    r.raise_for_status()
    return Release().load(r.json()["Releases"]["Data"], many=True)


def release(id, **kwargs):
    r = _session.get(f"{BASE_URL}/catalog/release/{id}", params=kwargs)
    r.raise_for_status()
    release = Release().load(r.json()["Release"])
    tracks = Track().load(r.json()["Tracks"], many=True)
    return {**release, "tracks": tracks}


def download_release_cover(catalog_id, outfile):
    download_file(f"https://www.monstercat.com/release/{catalog_id}/cover", outfile)


def download_track_url(release_id, track_id, file_format):
    r = _session.get(
        f"{BASE_URL}/release/{release_id}/track-download/{track_id}",
        params={"noRedirect": True, "format": file_format},
    )
    return r.json()["SignedUrl"]


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
