class Scenario(object):

    def __init__(self, description, given, when, then, before_each=list(), after_each=list()):
        self.description = description

        self.given = given if type(given) == list else [given]
        self.when = when if type(when) == list else [when]
        self.then = then if type(then) == list else [then]

        self.before_each = before_each if type(before_each) == list else [before_each]
        self.after_each = after_each if type(after_each) == list else [after_each]

        self.exception = None
        self.ran = False
        self.passed = False

    async def run(self, context):
        await self.__run_steps(context)

    async def __run_steps(self, context):
        try:
            for given in self.given:
                await self.__run_step(given, context)
            for when in self.when:
                await self.__run_step(when, context)
            for then in self.then:
                await self.__run_step(then, context)
        except Exception as e:
            self.exception = e
        else:
            self.passed = True
        finally:
            self.ran = True

    async def __run_step(self, step, context):
        await self.__run_before_each(context)
        await step.run(context)
        await self.__run_after_each(context)

    async def __run_before_each(self, context):
        for before in self.before_each:
            await before.run(context)

    async def __run_after_each(self, context):
        for after in self.after_each:
            await after.run(context)
