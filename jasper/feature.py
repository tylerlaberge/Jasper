from jasper.utility import cyan, red, indent
from jasper import Context


class Feature(object):

    def __init__(self, description, *scenarios):
        self.description = description
        self.scenarios = scenarios

        self.successes = []
        self.failures = []

    def __str__(self):
        color = cyan if not self.failures else red

        formatted_string = color(f'Feature: {self.description}\n')
        for scenario in self.scenarios:
            formatted_string += indent(f'{str(scenario)}\n', 4)

        return formatted_string

    def run(self):
        for scenario in self.scenarios:
            scenario(Context())
            scenario.run()

            if scenario.context.success:
                self.successes.append(scenario)
            else:
                self.failures.append(scenario)