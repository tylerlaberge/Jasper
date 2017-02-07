from jasper.utility import blue, red, indent
from jasper.exceptions import GivenException, WhenException, ThenException


class Scenario(object):

    def __init__(self, description, given, when, then):
        self.description = description

        self.given = given.cls(given.function)
        self.when = when.cls(when.function)
        self.then = then.cls(then.function)

        self.context = None
        self.exception = None
        self.passed = False

    def __call__(self, context):
        self.context = context

    def __str__(self):
        color = blue if self.passed else red
        scenario_string = color(f'Scenario: {self.description}\n')
        scenario_string += indent(f'{str(self.given)}\n', 4)
        if type(self.exception) is GivenException:
            scenario_string += indent(f'{str(self.exception)}\n', 4)

        scenario_string += indent(f'{str(self.when)}\n', 4)
        if type(self.exception) is WhenException:
            scenario_string += indent(f'{str(self.exception)}\n', 4)

        scenario_string += indent(f'{str(self.then)}', 4)
        if type(self.exception) is ThenException:
            scenario_string += indent(f'\n{str(self.exception)}', 4)

        return scenario_string

    async def run(self):
        await self.__run_steps()

    async def __run_steps(self):
        if self.context is not None:
            memento = self.context.commit()
            try:
                await self.given(self.context)
                await self.when(self.context)
                self.then(self.context)
            except (GivenException, WhenException, ThenException) as e:
                self.exception = e
            else:
                self.passed = True
            finally:
                self.context.unlock()
                self.context.rollback(memento)
