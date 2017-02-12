import click
from jasper.runner import Runner
from jasper.display import Display


@click.command()
@click.argument('test_directory', type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True))
@click.option('--ansi', is_flag=True, default=False, help="Flag to force display to use ansi escape sequences for coloring.")
def jasper(test_directory, ansi):
    runner = Runner(test_directory)
    completed_suite = runner.run()

    display = Display(force_ansi=ansi)
    display.prepare_suite(completed_suite)
    display.display()


if __name__ == '__main__':
    jasper()
