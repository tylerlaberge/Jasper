class Feature(object):

    def __init__(self, description, *scenarios):
        self.description = description
        self.scenarios = scenarios

    def run(self):
        for scenario in self.scenarios:
            scenario.run()
