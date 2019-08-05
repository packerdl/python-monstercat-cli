import click


@click.group()
@click.pass_context
def entry(ctx):
    """Command-line tool for the Monstercat Connect API"""
    pass
