import click
from jasper.runner import Runner


@click.command()
@click.argument('test_directory', type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True))
def jasper(test_directory):
    runner = Runner(test_directory)
    runner.run()


if __name__ == '__main__':
    jasper()
