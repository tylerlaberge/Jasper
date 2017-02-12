from jasper.utility import cyan, red, grey, indent
from jasper.exceptions import GivenException, WhenException, ThenException
import asyncio

class Scenario(object):

    def __init__(self, description, given, when, then):
        self.description = description

        self.given = given if type(given) == list else [given]
        self.when = when if type(when) == list else [when]
        self.then = then if type(then) == list else [then]

        self.context = None
        self.exception = None
        self.ran = False
        self.passed = False

    def __call__(self, context):
        self.context = context

    def __str__(self):
        if not self.ran:
            color = grey
        elif self.passed:
            color = cyan
        else:
            color = red

        scenario_string = color(f'Scenario: {self.description}')
        for given in self.given:
            scenario_string += indent(f'\n{str(given)}', 4)

        for when in self.when:
            scenario_string += indent(f'\n{str(when)}', 4)

        for then in self.then:
            scenario_string += indent(f'\n{str(then)}', 4)

        if self.exception is not None:
            scenario_string += indent(f'\n{str(self.exception)}', 4)

        scenario_string += '\n'
        return scenario_string

    async def run(self):
        await self.__run_steps()

    async def __run_steps(self):
        if self.context is not None:
            memento = self.context.commit()
            try:
                await asyncio.wait([given.run(self.context) for given in self.given])
                await asyncio.wait([when.run(self.context) for when in self.when])
                await asyncio.wait([then.run(self.context) for then in self.then])
            except (GivenException, WhenException, ThenException) as e:
                self.exception = e
            else:
                self.passed = True
            finally:
                self.ran = True
                self.context.unlock()
                self.context.rollback(memento)
