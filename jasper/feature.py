from jasper.context import Context
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

    @property
    def num_scenarios_passed(self):
        return len(self.successes)

    @property
    def num_scenarios_failed(self):
        return len(self.failures)

    async def run(self):
        context = Context()
        try:
            await self.__run_before_all(context)
            await asyncio.wait([self.__run_scenario(scenario, context.copy()) for scenario in self.scenarios])
            await self.__run_after_all(context)
        except Exception as e:
            self.exception = e
            self.passed = False

        return self

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
