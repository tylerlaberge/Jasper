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

    async def run(self):
        await self.__run_steps()

    async def __run_steps(self):
        if self.context is not None:
            memento = self.context.commit()
            try:
                for given in self.given:
                    await given.run(self.context)
                for when in self.when:
                    await when.run(self.context)
                for then in self.then:
                    await then.run(self.context)
            except Exception as e:
                self.exception = e
            else:
                self.passed = True
            finally:
                self.ran = True
                self.context.unlock()
                self.context.rollback(memento)
