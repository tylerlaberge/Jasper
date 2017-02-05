import click
import os
import astor
import ast


class Runner(object):

    def __init__(self, test_directory):
        self.test_directory = test_directory
        self.test_file_names = []

    def run(self):
        self.discover()
        self.parse()

    def discover(self):
        for dir_path, dir_names, files in os.walk(self.test_directory):
            for file_name in files:
                if file_name.lower().endswith('feature.py'):
                    self.test_file_names.append(os.path.join(dir_path, file_name))

    def parse(self):
        for test_file_name in self.test_file_names:
            with open(test_file_name, 'r') as test_file:
                exec(compile(str(test_file.read()), test_file_name, 'exec'), globals())


@click.command()
@click.argument('test_directory', type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True))
def jasper(test_directory):
    runner = Runner(test_directory)
    runner.run()

if __name__ == '__main__':
    jasper()