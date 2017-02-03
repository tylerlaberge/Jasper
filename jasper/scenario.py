from jasper.utility import cyan, red, indent


class Scenario(object):

    def __init__(self, description, given, when, then):
        self.description = description
        self.given = given
        self.when = when
        self.then = then

        self.context = None

    def __call__(self, context):
        self.context = context

    def __str__(self):
        color = cyan if self.context.success else red
        scenario_string = color(f'Scenario: {self.description}\n')
        given_string = color(indent(f'{str(self.given)}\n', 4))
        when_string = color(indent(f'{str(self.when)}\n', 4))
        then_string = color(indent(f'{str(self.then)}', 4))

        return scenario_string + given_string + when_string + then_string

    def run(self):
        if self.context is not None:
            self.given(self.context)
            self.when(self.context)
            self.then(self.context)
        else:
            raise ValueError
