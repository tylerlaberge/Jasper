from jasper import Context


class Feature(object):

    def __init__(self, description, *scenarios):
        self.description = description
        self.scenarios = scenarios

        self.successes = []
        self.failures = []

    def run(self):
        for scenario in self.scenarios:
            scenario(Context())
            scenario.run()

            if scenario.context.success:
                self.successes.append(scenario)
            else:
                self.failures.append(scenario)