from jasper.context import Context
from jasper.step import Step
from jasper.scenario import Scenario
from jasper.exceptions import ValidationException
import asyncio


class Feature(object):

    def __init__(self, description, scenarios, before_each=list(), before_all=list(), after_each=list(), after_all=list()):
        self.description = description
        self.scenarios = scenarios

        self.before_each = before_each if type(before_each) == list else [before_each]
        self.before_all = before_all if type(before_all) == list else [before_all]

        self.after_each = after_each if type(after_each) == list else [after_each]
        self.after_all = after_all if type(after_all) == list else [after_all]

        self.successes = []
        self.failures = []
        self.passed = True
        self.exception = None
        self.__validate()

    def __validate(self):
        for scenario in self.scenarios:
            if not isinstance(scenario, Scenario):
                raise ValidationException(f'\n\nFeature \'{self.description}\'. '
                                          f'Scenario: \'{scenario}\' must be an initialized Scenario object. '
                                          f'Instead got \'{type(scenario)}\'.')

        self.__validate_steps(self.before_each, 'BeforeEach')
        self.__validate_steps(self.after_each, 'AfterEach')
        self.__validate_steps(self.before_all, 'BeforeAll')
        self.__validate_steps(self.after_all, 'AfterAll')

    def __validate_steps(self, steps, step_type):
        for step in steps:
            if not isinstance(step, Step):
                raise ValidationException(f'\n\nFeature \'{self.description}\'. '
                                          f'{step_type}: \'{step}\' must be an initialized Step object. '
                                          f'Instead got \'{type(step)}\'. '
                                          f'Did you call the decorated step function?')

    @property
    def num_scenarios_passed(self):
        return len(self.successes)

    @property
    def num_scenarios_failed(self):
        return len(self.failures)

    async def run(self):
        context = Context()
        try:
            await self.__run_scenarios(context)
        except Exception as e:
            self.exception = e
            self.passed = False

        return self

    async def __run_scenarios(self, context):
        await self.__run_before_all(context)
        try:
            await asyncio.gather(*[self.__run_scenario(scenario, context.copy()) for scenario in self.scenarios])
        except Exception:
            raise
        finally:
            await self.__run_after_all(context)

    async def __run_scenario(self, scenario, context):
        await self.__run_before_each(context)
        await scenario.run(context)
        if scenario.passed:
            self.successes.append(scenario)
        else:
            self.failures.append(scenario)
            self.passed = False
        await self.__run_after_each(context)

    async def __run_before_all(self, context):
        for before in self.before_all:
            await before.run(context)

    async def __run_before_each(self, context):
        for before in self.before_each:
            await before.run(context)

    async def __run_after_all(self, context):
        for after in self.after_all:
            await after.run(context)

    async def __run_after_each(self, context):
        for after in self.after_each:
            await after.run(context)
