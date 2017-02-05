from jasper import JasperGiven, JasperWhen, JasperThen, Expect
import time


class Given(JasperGiven):

    def an_exception(self):
        raise Exception

    def a_slow_function(self):
        def sleep(amount):
            time.sleep(amount)

        self.context.sleep = sleep

    def an_adding_function(self):
        def add(a, b):
            return a + b

        self.context.function = add

    def a_multiplication_function(self):
        def multiply(a, b):
            return a * b

        self.context.function = multiply


class When(JasperWhen):
    def we_call_it_with_two_negative_numbers(self):
        self.context.result = self.context.function(-5, -5)

    def we_call_it_with_two_positive_numbers(self):
        self.context.result = self.context.function(5, 5)

    def we_call_it_with_two_strings(self):
        try:
            self.context.function('foo', 'bar')
        except Exception as e:
            self.context.result = e
        else:
            self.context.result = None

    def we_raise_an_exception(self):
        raise Exception

    def we_call_it_with_some_number(self):
        self.context.sleep(3)
        self.context.slept = True


class Then(JasperThen):
    def we_will_get_a_negative_number(self):
        Expect(self.context.result).to_be.less_than(0)

    def we_will_get_a_positive_number(self):
        Expect(self.context.result).to_be.greater_than(0)

    def a_typeerror_will_occur(self):
        Expect(self.context.result.__class__).to_be(TypeError)

    def we_will_have_slept(self):
        Expect(self.context.slept).to_be(True)