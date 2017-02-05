from jasper import JasperGiven, JasperWhen, JasperThen, Expect


class Given(JasperGiven):

    def some_other_step(self):
        def other_step():
            return 'FOOBAR'

        self.context.other_step = other_step


class When(JasperWhen):

    def we_call_it(self):
        self.context.result = self.context.other_step()


class Then(JasperThen):
    def we_will_get_foobar(self):
        Expect(self.context.result).to_be('FOOBAR')