from jasper.utility import blue, red, indent
from jasper import Context


class Feature(object):

    def __init__(self, description, *scenarios):
        self.description = description
        self.scenarios = scenarios

        self.successes = []
        self.failures = []
        self.passed = True

    @property
    def num_scenarios_passed(self):
        return len(self.successes)

    @property
    def num_scenarios_failed(self):
        return len(self.failures)

    def __str__(self):
        color = blue if not self.failures else red

        formatted_string = color(f'Feature: {self.description}\n')
        for scenario in self.scenarios:
            formatted_string += indent(f'{str(scenario)}\n', 4)

        formatted_string += color(f'\n{self.num_scenarios_passed} Scenarios passed, {self.num_scenarios_failed} failed.')
        return formatted_string

    def run(self):
        for scenario in self.scenarios:
            scenario(Context())
            scenario.run()

            if scenario.passed:
                self.successes.append(scenario)
            else:
                self.failures.append(scenario)
                self.passed = False
