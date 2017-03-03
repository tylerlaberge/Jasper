"""
The display module.
"""

from jasper.utility import extract_traceback
from termcolor import colored
import textwrap
import colorama
import sys


class Display(object):
    """
    The class responsible for displaying the results of a suites, features, scenarios, and steps.
    """
    def __init__(self, force_ansi=True, verbosity_level=0):
        """
        Initialize a new Display object.

        :param force_ansi: Flag for whether or not to force the display to use ansi escape sequences. default is True.
        :param verbosity_level:  The verbosity level for the display to use. default is 0, maxes out at 2.
        """
        self.display_string = ''
        self.indentation_level = 0
        self.verbosity_level = verbosity_level
        self.colored = True
        self.force_ansi = force_ansi
        colorama.deinit()

    def display(self):
        """
        Print the prepared data to the screen.
        """
        if sys.platform == 'win32' and not self.force_ansi:
            colorama.init()
        print(self.display_string)
        colorama.deinit()

    def cyan(self, text):
        """
        Color some text cyan.

        If the displays color is disabled the text will not be colorized.

        :param text: The text to color.
        :return: The colored text
        """
        return colored(text, 'cyan') if self.colored else text

    def yellow(self, text):
        """
        Color some text yellow.

        If the displays color is disabled the text will not be colorized.

        :param text: The text to color.
        :return: The colored text
        """
        return colored(text, 'yellow') if self.colored else text

    def red(self, text):
        """
        Color some text red.

        If the displays color is disabled the text will not be colorized.

        :param text: The text to color.
        :return: The colored text
        """
        return colored(text, 'red') if self.colored else text

    def grey(self, text):
        """
        Color some text grey.

        If the displays color is disabled the text will not be colorized.

        :param text: The text to color.
        :return: The colored text
        """
        return colored(text, 'white') if self.colored else text

    @staticmethod
    def indent(text, amount):
        """
        Indent some text by the given amount.

        :param text: The text to indent.
        :param amount: The amount of spaces to indent the text with.
        :return: The indented text.
        """
        return textwrap.indent(text, ' ' * amount)

    def __push_to_display(self, display_string):
        self.display_string += self.indent(display_string + '\n', self.indentation_level)

    def prepare_suite(self, suite):
        """
        Prepare a Suite object to be displayed.

        :param suite: The Suite to prepare.
        """
        color = self.cyan if suite.passed else self.red

        if not suite.passed or self.verbosity_level > 0:
            for feature in suite.features:
                self.prepare_feature(feature)
        self.__push_to_display(self.prepare_border(color, 150))
        self.prepare_statistics(suite)
        self.__push_to_display(self.prepare_border(color, 150))

    def prepare_feature(self, feature):
        """
        Prepare a Feature object to be displayed.

        :param feature: The Feature to prepare.
        """
        if not feature.passed or self.verbosity_level > 0:
            color = self.cyan if feature.passed else self.red

            self.__push_to_display(self.prepare_border(color, 150))
            self.__push_to_display(color(f'Feature: {feature.description}'))

            self.indentation_level += 4
            if not feature.passed or self.verbosity_level > 1:
                for before in feature.before_all:
                    self.prepare_step(before, 'BeforeAll')
                for after in feature.after_all:
                    self.prepare_step(after, 'AfterAll')
                for before in feature.before_each:
                    self.prepare_step(before, 'BeforeEach')
                for after in feature.after_each:
                    self.prepare_step(after, 'AfterEach')
            for scenario in feature.scenarios:
                self.prepare_scenario(scenario)
            if feature.exception is not None:
                self.prepare_exception(feature.exception)
            self.indentation_level -= 4

            self.__push_to_display(self.prepare_border(color, 150))

    def prepare_scenario(self, scenario):
        """
        Prepare a Scenario object to be displayed.

        :param scenario: The Scenario to prepare.
        """
        if not scenario.passed or self.verbosity_level > 0:
            if not scenario.ran:
                color = self.grey
            elif scenario.passed:
                color = self.cyan
            else:
                color = self.red

            self.__push_to_display(color(f'Scenario: {scenario.description}'))
            if not scenario.passed or self.verbosity_level > 1:
                self.indentation_level += 4
                for before in scenario.before_all:
                    self.prepare_step(before, 'BeforeAll')
                for after in scenario.after_all:
                    self.prepare_step(after, 'AfterAll')
                for before in scenario.before_each:
                    self.prepare_step(before, 'BeforeEach')
                for after in scenario.after_each:
                    self.prepare_step(after, 'AfterEach')
                for index, given in enumerate(scenario.given):
                    self.prepare_step(given, 'Given') if index == 0 else self.prepare_step(given, 'And')
                for index, when in enumerate(scenario.when):
                    self.prepare_step(when, 'When') if index == 0 else self.prepare_step(when, 'And')
                for index, then in enumerate(scenario.then):
                    self.prepare_step(then, 'Then') if index == 0 else self.prepare_step(then, 'And')
                if scenario.exception is not None:
                    self.prepare_exception(scenario.exception)
                self.indentation_level -= 4

    def prepare_step(self, step, step_name):
        """
        Prepare a Step object to be displayed.

        :param step: The Step to prepare.
        :param step_name: A name to represent the step with.
        """
        if not step.ran:
            color = self.grey
        elif step.passed:
            color = self.cyan
        else:
            color = self.red

        self.__push_to_display(color(f"{step_name}: "
                                     f"{step.function.__name__} {step.kwargs if step.kwargs else ''}"))

    def prepare_exception(self, exception):
        """
        Prepare an exception to be displayed.

        :param exception: The exception to prepare.
        """
        if str(exception):
            exception_string = f'{str(exception)}\n'
        else:
            exception_string = f'{exception.__class__.__name__}\n'

        traceback_string = f'{extract_traceback(exception)}'

        self.__push_to_display(self.yellow((exception_string + traceback_string).rstrip()))

    def prepare_border(self, color, length):
        """
        Prepare a border to be displayed.

        :param color: The color to give the border.
        :param length: The length of the border.
        """
        return color('=' * length)

    def prepare_statistics(self, suite):
        """
        Prepare the statistics of a Suite object to be displayed.

        :param suite: The Suite object to prepare the statistics for.
        """
        color = self.cyan if suite.passed else self.red

        self.__push_to_display(
            color(
                f'{suite.num_features_passed} Features passed, {suite.num_features_failed} failed.\n'
                f'{suite.num_scenarios_passed} Scenarios passed, {suite.num_scenarios_failed} failed.'
            )
        )
