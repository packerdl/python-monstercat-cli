import math
import time
from pathlib import Path

import click
from halo import Halo

from . import api, settings


def progress_callback(progress, spinner, name):
    spinner.text = f"[Downloading - {math.floor(progress * 100)}%] - {name}"


@click.command()
@click.option(
    "--file-format",
    help="Override preferred format",
    type=click.Choice(["mp3_128", "mp3_v0", "mp3_v2", "mp3_320", "flac", "wav"]),
)
@click.option("--catalog-path", help="Override catalog location", type=click.Path())
def sync(file_format, catalog_path):
    file_format = file_format or settings.config["format"]
    extension = file_format.split("_")[0].lower()
    if not catalog_path:
        catalog_path = Path(settings.config["catalog_path"])
    catalog_path.mkdir(parents=True, exist_ok=True)

    skip = 0
    limit = 10
    releases = api.releases(offset=skip, limit=limit)
    while len(releases) > 0:
        for release in releases:
            release_folder_name = f"{release['artists_title']} - {release['title']}"
            if "catalog_id" in release:
                release_folder_name = f"{release['catalog_id']} - {release_folder_name}"

            if release["in_early_access"]:
                print(f"{release_folder_name} - Skipped (Early Access)")
                continue

            print(release_folder_name)

            release_folder_path = catalog_path / release_folder_name
            release_folder_path.mkdir(parents=True, exist_ok=True)

            cover_path = release_folder_path / "cover.jpg"
            if not cover_path.exists():
                api.download_release_cover(release["catalog_id"], cover_path)

            tracks = api.release(release["catalog_id"])["tracks"]
            for track in tracks:
                track_filename = (
                    f"{track['track_number']:02} - {track['artists_title']} - "
                    f"{track['title']}.{extension}"
                )
                track_path = release_folder_path / track_filename

                spinner = Halo(text=f"[Downloading - 0%] {track_filename}")
                spinner.start()

                if track_path.exists():
                    spinner.succeed(f"{track_filename} - Skipped (Already Exists)")
                    continue

                download_url = api.download_track_url(
                    release["id"], track["id"], file_format
                )

                try:
                    api.download_file(
                        download_url,
                        track_path,
                        callback=(
                            lambda p: progress_callback(p, spinner, track_filename)
                        ),
                    )
                    spinner.succeed(track_filename)
                except Exception as e:
                    spinner.fail(f"{track_filename}\n{e}")

                # Be nice to the Monstercat servers!
                time.sleep(1)

        skip += limit

        # Be nice to the Monstercat servers!
        time.sleep(5)
        releases = api.releases(offset=skip, limit=limit)
