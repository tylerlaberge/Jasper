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

        self.__validate()

    def __call__(self, context):
        self.context = context

    def __validate(self):
        for given in self.given:
            if given.step_type != 'Given':
                raise ValueError(
                    f'Scenario \'{self.description}\': '
                    f'\'{given.function.__name__}\' step is of type \'{given.step_type}\', should be of type \'Given\''
                )
        for when in self.when:
            if when.step_type != 'When':
                raise ValueError(
                    f'Scenario \'{self.description}\': '
                    f'\'{when.function.__name__}\' step is of type \'{when.step_type}\', should be of type \'When\''
                )
        for then in self.then:
            if then.step_type != 'Then':
                raise ValueError(
                    f'Scenario \'{self.description}\': '
                    f'\'{then.function.__name__}\' step is of type \'{then.step_type}\', should be of type \'Then\''
                )

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
                self.context.rollback(memento)
