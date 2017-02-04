from jasper.utility import cyan, red


class Suite(object):

    def __init__(self, *features):
        self.features = features
        self.successes = []
        self.failures = []

    def __str__(self):
        formatted_string = ''
        for feature in self.successes:
            formatted_string += cyan('='*150) + '\n'
            formatted_string += f'{feature}'
            formatted_string += cyan('=' * 150) + '\n'

        for feature in self.failures:
            formatted_string += red('=' * 150) + '\n'
            formatted_string += f'{feature}'
            formatted_string += red('=' * 150) + '\n'

        return formatted_string

    def run(self):
        for feature in self.features:
            feature.run()

            if feature.passed:
                self.successes.append(feature)
            else:
                self.failures.append(feature)
