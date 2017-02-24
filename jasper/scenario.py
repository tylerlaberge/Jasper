from jasper.steps import Step
from jasper.exceptions import ValidationException


class Scenario(object):

    def __init__(self, description, given, when, then,
                 before_each=list(), before_all=list(), after_each=list(), after_all=list()):
        self.description = description

        self.given = given if type(given) == list else [given]
        self.when = when if type(when) == list else [when]
        self.then = then if type(then) == list else [then]

        self.before_each = before_each if type(before_each) == list else [before_each]
        self.before_all = before_all if type(before_all) == list else [before_all]

        self.after_each = after_each if type(after_each) == list else [after_each]
        self.after_all = after_all if type(after_all) == list else [after_all]

        self.exception = None
        self.ran = False
        self.passed = False

        self.__validate()

    def __validate(self):
        self.__validate_steps(self.given, 'Given')
        self.__validate_steps(self.when, 'When')
        self.__validate_steps(self.then, 'Then')
        self.__validate_steps(self.before_each, 'BeforeEach')
        self.__validate_steps(self.after_each, 'AfterEach')
        self.__validate_steps(self.before_all, 'BeforeAll')
        self.__validate_steps(self.after_all, 'AfterAll')

    def __validate_steps(self, steps, step_type):
        for step in steps:
            if not isinstance(step, Step):
                raise ValidationException(f'\n\nScenario \'{self.description}\'. '
                                          f'{step_type}: \'{step}\' must be an initialized Step object. '
                                          f'Instead got \'{type(step)}\'. '
                                          f'Did you call the decorated step function?')

    async def run(self, context):
        try:
            await self.__run_steps(context)
        except Exception as e:
            self.exception = e
        else:
            self.passed = True
        finally:
            self.ran = True

    async def __run_steps(self, context):
        await self.__run_before_all(context)
        try:
            for given in self.given:
                await self.__run_step(given, context)
            for when in self.when:
                await self.__run_step(when, context)
            for then in self.then:
                await self.__run_step(then, context)
        except Exception:
            raise
        finally:
            await self.__run_after_all(context)

    async def __run_step(self, step, context):
        await self.__run_before_each(context)
        try:
            await step.run(context)
        except Exception:
            raise
        finally:
            await self.__run_after_each(context)

    async def __run_before_each(self, context):
        for before in self.before_each:
            await before.run(context)

    async def __run_before_all(self, context):
        for before in self.before_all:
            await before.run(context)

    async def __run_after_each(self, context):
        for after in self.after_each:
            await after.run(context)

    async def __run_after_all(self, context):
        for after in self.after_all:
            await after.run(context)
