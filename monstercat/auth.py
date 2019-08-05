import click
from halo import Halo
from requests import HTTPError

from . import api, settings


@click.command()
@click.option('--email', prompt='Monstercat Email')
@click.option('--password', prompt='Monstercat Password', hide_input=True)
def login(email, password):
    spinner = Halo(text="Logging into Monstercat", spinner="dots").start()
    try:
        response = api.login(email, password)
        settings.set("cookie", dict(response.cookies))
        spinner.succeed("Successfully logged into Monstercat")
    except HTTPError as e:
        body = e["response"].json()
        if "invalid email" in body["message"] \
                or "invalid password" in body["message"]:
            spinner.fail("Incorrect email or password")
        else:
            spinner.fail("Unable to login: Unexpected API response")
    except Exception as e:
        spinner.fail("An exception occurred")
        print(e)


@click.command()
def logout():
    spinner = Halo(text="Logging out of Monstercat...", spinner="dots").start()
    api.logout()
    settings.clear("cookie")
    spinner.succeed("Logged out of Monstercat")


@click.command()
def status():
    spinner = Halo(text="Checking session...", spinner="dots").start()
    try:
        session = api.session()
        if "user" in session:
            spinner.succeed("Logged in to Monstercat")
            if "download" in session["permissions"]["catalog"]:
                Halo().succeed("Monstercat Gold Subscriber")
            else:
                Halo().fail("Account does not have Monstercat Gold")
        else:
            spinner.fail("Not logged in to Monstercat")
    except Exception as e:
        spinner.fail("An exception occurred")
        print(e)
