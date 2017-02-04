from jasper.utility import cyan, red, yellow, indent
from jasper.exceptions import GivenException, WhenException, ThenException


class Scenario(object):

    def __init__(self, description, given, when, then):
        self.description = description
        self.given = given
        self.when = when
        self.then = then

        self.context = None
        self.exception = None
        self.passed = False

    def __call__(self, context):
        self.context = context

    def __str__(self):
        color = cyan if self.passed else red
        scenario_string = color(f'Scenario: {self.description}\n')
        scenario_string += indent(f'{str(self.given)}\n', 4)
        scenario_string += indent(f'{str(self.when)}\n', 4)
        scenario_string += indent(f'{str(self.then)}', 4)

        if self.exception:
            scenario_string += yellow(indent(f'\n\n{str(self.exception)}', 4))

        return scenario_string

    def run(self):
        if self.context is not None:
            try:
                self.given(self.context)
                self.when(self.context)
                self.then(self.context)
            except (GivenException, WhenException, ThenException) as e:
                self.exception = e
            else:
                self.passed = True
        else:
            raise ValueError
