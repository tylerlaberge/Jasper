class Scenario(object):

    def __init__(self, description, given, when, then):
        self.description = description
        self.given = given
        self.when = when
        self.then = then

        self.context = None

    def __call__(self, context):
        self.context = context

    def run(self):
        if self.context is not None:
            self.given(self.context)
            self.when(self.context)
            self.then(self.context)
        else:
            raise ValueError
