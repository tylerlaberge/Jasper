from abc import ABCMeta, abstractmethod
from termcolor import colored
import textwrap
from jasper.utility import extract_traceback


class View(object, metaclass=ABCMeta):

    def cyan(self, text):
        return colored(text, 'cyan')

    def magenta(self, text):
        return colored(text, 'magenta')

    def yellow(self, text):
        return colored(text, 'yellow')

    def red(self, text):
        return colored(text, 'red')

    def grey(self, text):
        return colored(text, 'white')

    @staticmethod
    def indent(text, amount):
        return textwrap.indent(text, ' ' * amount)

    @abstractmethod
    def display(self):
        pass


class ExceptionView(View):

    def __init__(self, exception):
        self.exception = exception

    def display(self):
        if str(self.exception):
            exception_string = f'{str(self.exception)}\n'
        else:
            exception_string = f'{self.exception.__class__.__name__}\n'

        traceback_string = f'{extract_traceback(self.exception)}'

        print(
            self.yellow(
                (exception_string + traceback_string).rstrip()
            )
        )


class StepView(View):

    def __init__(self, step):
        self.step = step

    def display(self):
        if not self.step.ran:
            color = self.grey
        elif self.step.passed:
            color = self.cyan
        else:
            color = self.red

        print(
            color(
                f"{self.step.__class__.__name__}: "
                f"{self.step.function.__name__} {self.step.kwargs if self.step.kwargs else ''}"
            )
        )


class ScenarioView(View):

    def __init__(self, scenario):
        self.scenario = scenario
        self.given_views = [StepView(given) for given in self.scenario.given]
        self.when_views = [StepView(when) for when in self.scenario.when]
        self.then_views = [StepView(then) for then in self.scenario.then]
        self.exception_view = ExceptionView(scenario.exception) if scenario.exception else None

    def display(self):
        if not self.scenario.ran:
            color = self.grey
        elif self.scenario.passed:
            color = self.cyan
        else:
            color = self.red

        print(
            color(
                f'Scenario: {self.scenario.description}'
            )
        )

        self.indent('', 4)
        for given_view in self.given_views:
            given_view.display()
        for when_view in self.when_views:
            when_view.display()
        for then_view in self.then_views:
            then_view.display()
        if self.exception_view is not None:
            self.exception_view.display()
        self.indent('', -4)


class FeatureView(View):

    def __init__(self, feature):
        self.feature = feature
        self.before_each_views = [StepView(before) for before in self.feature.before_each] if self.feature.before_each else []
        self.after_each_views = [StepView(after) for after in self.feature.after_each] if self.feature.after_each else []
        self.scenario_views = [ScenarioView(scenario) for scenario in self.feature.scenarios]
        self.exception_view = ExceptionView(self.feature.exception) if self.feature.exception else None

    def display(self):
        color = self.cyan if self.feature.passed else self.red

        print(
            color(
                f'Feature: {self.feature.description}'
            )
        )

        self.indent('', 4)
        for before_each_view in self.before_each_views:
            before_each_view.display()
        for scenario_view in self.scenario_views:
            scenario_view.display()

        if self.exception_view is not None:
            self.exception_view.display()
        self.indent('', -4)


class SuiteView(View):

    def __init__(self, suite):
        self.suite = suite
        self.feature_views = [FeatureView(feature) for feature in self.suite.features]

    def display(self):
        color = self.cyan if self.suite.passed else self.red

        for feature_view in self.feature_views:
            feature_view.display()

        print(
            color(
                f'{self.suite.num_features_passed} Features passed, {self.suite.num_features_failed} failed.\n'
                f'{self.suite.num_scenarios_passed} Scenarios passed, {self.suite.num_scenarios_failed} failed'
            )
        )
