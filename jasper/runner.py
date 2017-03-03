"""
The runner module.
"""

import asyncio
import os
import importlib.util
from jasper.suite import Suite
from jasper.feature import Feature
import time


class Runner(object):
    """
    The class responsible for finding, building, and running features.
    """
    def __init__(self, test_directory):
        """
        Initialize a new Runner object.

        :param test_directory: The directory to search for feature files in.
        """
        self.test_directory = test_directory
        self.test_file_paths = []
        self.suite = Suite()

    def run(self):
        """
        Discover the feature files, build the suite, and run the tests.

        :return: The Suite that has been built and run.
        """
        self.discover()
        self.build_suite()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.suite.run())
        loop.close()
        time.sleep(0.5)
        return self.suite

    def discover(self):
        """
        Find any feature files within the given test directory.
        """
        for dir_path, dir_names, files in os.walk(self.test_directory):
            for file_name in files:
                if file_name.lower().endswith('feature.py'):
                    self.test_file_paths.append(os.path.join(dir_path, file_name))

    def build_suite(self):
        """
        Build a Suite object out of the Features contained within the found feature files.
        """
        for test_file_path in self.test_file_paths:
            spec = importlib.util.spec_from_file_location("module.name", test_file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            for name in dir(module):
                obj = getattr(module, name)
                if isinstance(obj, Feature):
                    self.suite.add_feature(obj)
