import click
from jasper.runner import Runner
from jasper.display import Display


@click.command()
@click.argument('test_directory', type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True))
@click.option('--ansi', is_flag=True, default=False, help="Flag to force display to use ansi escape sequences for coloring.")
@click.option('-v', type=click.IntRange(0, 2), default=1, help="Verbosity level from 0 to 2. default is 0.")
def jasper(test_directory, ansi, v):
    runner = Runner(test_directory)
    completed_suite = runner.run()

    display = Display(force_ansi=ansi, verbosity_level=v)
    display.prepare_suite(completed_suite)
    display.display()


if __name__ == '__main__':
    jasper()
