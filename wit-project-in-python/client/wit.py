
import click
import core as wit
@click.group()
def cli():
    pass


@cli.command()
def init():
    click.echo(wit.init_repo())


@cli.command()
@click.argument("path")
def add(path):
    click.echo(wit.add(path))


@cli.command()
@click.option("-m", "--message", required=True)
def commit(message):
    click.echo(wit.commit(message))


@cli.command()
def status():
    staged, untracked = wit.status()
    click.echo("\n--- Status ---")
    click.echo("Staged files:")
    for f in staged:
        click.echo(f"  {f}")
    click.echo("\nUntracked files:")
    for f in untracked:
        click.echo(f"  {f}")


@cli.command()
@click.argument("commit_id")
def checkout(commit_id):
    click.echo(wit.checkout(commit_id))

@cli.command()
def push():
    click.echo(wit.push())

if __name__ == "__main__":
    cli()


