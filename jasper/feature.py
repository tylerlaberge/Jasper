from jasper.context import Context
import asyncio


class Feature(object):

    def __init__(self, description, *scenarios, before_each=None):
        self.description = description
        self.scenarios = scenarios
        if before_each is not None:
            self.before_each = before_each if type(before_each) == list else [before_each]
        else:
            self.before_each = before_each
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
        await asyncio.wait([self.__run_scenario(scenario) for scenario in self.scenarios])
        return self

    async def __run_scenario(self, scenario):
        context = Context()
        if self.before_each is not None:
            try:
                for before in self.before_each:
                    await before.run(context)
            except Exception as e:
                self.exception = e
                self.passed = False
                return

        scenario(context)
        await scenario.run()

        if scenario.passed:
            self.successes.append(scenario)
        else:
            self.failures.append(scenario)
            self.passed = False
