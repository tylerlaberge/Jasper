class Given(Jasper.Given):

    def an_adding_function(self, context, a, b):
        context.result = a + b

    def a_multiplication_function(self, context, a, b):
        context.result = a * b


class When(Jasper.When):

    def we_call_it_with_two_negative_numbers(self, context):
        context.function(-5, -5)

    def we_call_it_with_two_positive_numbers(self, context):
        context.function(5, 5)


class Then(Jasper.Then):

    def we_will_get_a_negative_number(self, context):
        Expect(context.result).to_be.less_than(0)

    def we_will_get_a_positive_number(self, context):
        Expect(context.result).to_be.greater_than(0)

Jasper.Scenario(
    given={
        'function': Given.an_adding_function
    },
    when=When.we_call_it_with_two_negative_numbers,
    then=Then.we_will_get_a_negative_number
)
Jasper.Scenario(
    given={
        'function': Given.an_adding_function
    },
    when=When.we_call_it_with_two_positive_numbers,
    then=Then.we_will_get_a_positive_number
)
Jasper.Scenario(
    given={
        'function': Given.a_multiplication_function
    },
    when=When.we_call_it_with_two_negative_numbers,
    then=Then.we_will_get_a_positive_number
)


