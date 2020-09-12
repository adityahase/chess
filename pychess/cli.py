import click

from pychess.uci import UCI


@click.command()
def cli():
    uci = UCI()
    uci.run()
