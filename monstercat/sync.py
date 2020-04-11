import math
import os
import time

import click
from halo import Halo

from . import api, settings


def progress_callback(progress, spinner, name):
    spinner.text = f"[Downloading - {math.floor(progress * 100)}%] - {name}"


@click.command()
@click.option(
    "--file-format",
    help="Override preferred format",
    type=click.Choice(["mp3_128", "mp3_v0", "mp3_v2", "mp3_320", "flac", "wav"])
)
@click.option(
    "--catalog-path",
    help="Override catalog location",
    type=click.Path()
)
def sync(file_format, catalog_path):
    catalog_path = catalog_path or settings.config["catalog_path"]
    file_format = file_format or settings.config["format"]
    if not os.path.isdir(catalog_path):
        os.makedirs(catalog_path)
    skip = 0
    limit = 10
    releases = api.releases(skip=skip, limit=limit)
    while len(releases["results"]) > 0:
        for release in releases["results"]:
            name = f"{release['catalogId'] or release['artistsTitle']} - {release['title']}"
            filename = f"{name}.zip"
            download_link = api.generate_release_link(release["id"], file_format)
            outfile = os.path.join(catalog_path, filename)
            spinner = Halo(text=f"[Downloading - 0%] {name}")

            if release["inEarlyAccess"]:
                spinner.warn(f"[Skipping: Early Access] {name}")
                continue
            elif os.path.exists(outfile):
                spinner.succeed(f"[Already Exists] {name}")
                continue

            spinner.start()
            try:
                api.download_file(
                    download_link, outfile,
                    callback=(lambda p: progress_callback(p, spinner, name))
                )
                spinner.succeed(f"[Downloaded] {name}")
            except Exception as e:
                spinner.fail(f"[Failed] {name}\n{e}")
        skip += limit
        releases = api.releases(skip=skip, limit=limit)
        time.sleep(5)
