class Scenario(object):

    def __init__(self, description, given, when, then):
        self.description = description

        self.given = given if type(given) == list else [given]
        self.when = when if type(when) == list else [when]
        self.then = then if type(then) == list else [then]

        self.exception = None
        self.ran = False
        self.passed = False

    async def run(self, context):
        await self.__run_steps(context)

    async def __run_steps(self, context):
        try:
            for given in self.given:
                await given.run(context)
            for when in self.when:
                await when.run(context)
            for then in self.then:
                await then.run(context)
        except Exception as e:
            self.exception = e
        else:
            self.passed = True
        finally:
            self.ran = True
