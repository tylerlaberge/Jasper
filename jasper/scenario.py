from jasper.utility import cyan, red, indent
from jasper.exceptions import ThenException


class Scenario(object):

    def __init__(self, description, given, when, then):
        self.description = description
        self.given = given
        self.when = when
        self.then = then

        self.context = None
        self.exception = None

    def __call__(self, context):
        self.context = context

    def __str__(self):
        color = cyan if self.context.success else red
        scenario_string = color(f'Scenario: {self.description}\n')
        scenario_string += color(indent(f'{str(self.given)}\n', 4))
        scenario_string += color(indent(f'{str(self.when)}\n', 4))
        scenario_string += color(indent(f'{str(self.then)}\n', 4))

        if self.exception:
            scenario_string += color(indent(f'\n{str(self.exception)}', 4))

        return scenario_string

    def run(self):
        if self.context is not None:
            try:
                self.given(self.context)
                self.when(self.context)
                self.then(self.context)
            except ThenException as e:
                self.exception = e
        else:
            raise ValueError
