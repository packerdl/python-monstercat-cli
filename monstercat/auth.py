import click
from halo import Halo
from requests import HTTPError

from . import api, settings


@click.command()
@click.option("--email", prompt="Monstercat Email", help="Monstercat email")
@click.option(
    "--password",
    prompt="Monstercat Password",
    hide_input=True,
    help="Monstercat password",
)
def login(email, password):
    """Authenticate and create session"""
    spinner = Halo(text="Logging into Monstercat", spinner="dots").start()
    try:
        response = api.login(email, password)
        settings.set("cookie", dict(response.cookies))
        spinner.succeed("Successfully logged into Monstercat")
    except HTTPError as e:
        body = e.response.json()
        if "name" in body and "Invalid password or email" in body["name"]:
            spinner.fail("Incorrect email or password")
        else:
            spinner.fail("Unable to login: Unexpected API response")
    except Exception as e:
        spinner.fail("An exception occurred")
        print(e)


@click.command()
def logout():
    """Clear session information"""
    spinner = Halo(text="Logging out of Monstercat...", spinner="dots").start()
    api.logout()
    settings.clear("cookie")
    spinner.succeed("Logged out of Monstercat")


@click.command()
def status():
    """Check session and download permissions"""
    spinner = Halo(text="Checking session...", spinner="dots").start()
    try:
        session = api.session()
        if "User" in session:
            spinner.succeed("Logged in to Monstercat")
            if session["User"]["HasGold"]:
                Halo().succeed("Monstercat Gold Subscriber")
            else:
                Halo().fail("Account does not have Monstercat Gold")
        else:
            spinner.fail("Not logged in to Monstercat")
    except Exception as e:
        spinner.fail("An exception occurred")
        print(e)
