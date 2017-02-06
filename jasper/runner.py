import click
import os
import importlib.util
from jasper import Suite, Feature


class Runner(object):

    def __init__(self, test_directory):
        self.test_directory = test_directory
        self.test_file_paths = []
        self.suite = Suite()

    def run(self):
        self.discover()
        self.build_suite()
        self.suite.run()
        print(self.suite)

    def discover(self):
        for dir_path, dir_names, files in os.walk(self.test_directory):
            for file_name in files:
                if file_name.lower().endswith('feature.py'):
                    self.test_file_paths.append(os.path.join(dir_path, file_name))

    def build_suite(self):
        for test_file_path in self.test_file_paths:
            spec = importlib.util.spec_from_file_location("module.name", test_file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            for name in dir(module):
                obj = getattr(module, name)
                if isinstance(obj, Feature):
                    self.suite.add_feature(obj)


@click.command()
@click.argument('test_directory', type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True))
def jasper(test_directory):
    runner = Runner(test_directory)
    runner.run()

if __name__ == '__main__':
    jasper()