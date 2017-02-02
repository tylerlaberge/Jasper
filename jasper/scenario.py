from jasper import Context


class Scenario(object):

    def __init__(self, description, given, when, then):
        self.description = description
        self.given = given
        self.when = when
        self.then = then

        self.context = Context()

        self.prepared_given = False
        self.ran_when = False
        self.ran_then = False

    def prepare_given(self):
        self.given(self.context)
        self.prepared_given = True

    def run_when(self):
        if self.prepared_given:
            self.when(self.context)
            self.ran_when = True
        else:
            raise ValueError

    def run_then(self):
        if self.ran_when:
            self.then(self.context)
            self.ran_then = True
        else:
            raise ValueError

    def run(self):
        self.prepare_given()
        self.run_when()
        self.run_then()
