from . import ensure_server_from_files
import click

@click.group()
# @click.option('--debug/--no-debug', default=False)
def cli():
    pass

# @cli.option('--help')
# def print_help_msg(command):
#     with click.Context(command) as ctx:
#         click.echo(cli.get_help(ctx))

@cli.command()
@click.option('-d', '--destination', default=".", type=click.Path())
@click.option('-r', '--registry', type=click.Path())
@click.option('-s', '--state', type=click.Path())
def ensure(registry, state, destination):
    ensure_server_from_files(registry, state, destination)
