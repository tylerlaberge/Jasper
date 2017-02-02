from jasper import Expect


class Given(Jasper.Given):

    def an_adding_function(self, a, b):
        return a + b

    def a_multiplication_function(self, a, b):
        return a * b

    def some_class(self):

        class foo(object):
            def bar(self):
                pass

        return foo


class When(Jasper.When):

    def we_call_it_with_two_negative_numbers(self):
        return self.context.function(-5, -5)

    def we_call_it_with_two_positive_numbers(self):
        return self.context.function(5, 5)


class Then(Jasper.Then):

    def we_will_get_a_negative_number(self):
        Expect(self.context.result).to_be.less_than(0)

    def we_will_get_a_positive_number(self):
        Expect(self.context.result).to_be.greater_than(0)


Jasper.Scenario(
    Given('an_adding_function', with_alias='function'),
    When('we_call_it_with_two_negative_numbers'),
    Then('we_will_get_a_negative_number')
)



