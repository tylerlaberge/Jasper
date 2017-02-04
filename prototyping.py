from jasper import Suite, Feature, Scenario, JasperGiven, JasperWhen, JasperThen, Expect


class Given(JasperGiven):

    def an_exception(self):
        raise Exception

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


class Then(JasperThen):
    def we_will_get_a_negative_number(self):
        Expect(self.context.result).to_be.less_than(0)

    def we_will_get_a_positive_number(self):
        Expect(self.context.result).to_be.greater_than(0)

    def a_typeerror_will_occur(self):
        Expect(self.context.result.__class__).to_be(TypeError)

suite = Suite(
    Feature(
        'Arithmetic',
        Scenario(
            'Adding two negative numbers',
            Given('an_adding_function'),
            When('we_call_it_with_two_negative_numbers'),
            Then('we_will_get_a_negative_number')
        ),
        Scenario(
            'Adding two positive numbers',
            Given('an_adding_function'),
            When('we_call_it_with_two_positive_numbers'),
            Then('we_will_get_a_positive_number')
        ),
        Scenario(
            'Multiplying two strings',
            Given('a_multiplication_function'),
            When('we_call_it_with_two_strings'),
            Then('a_typeerror_will_occur')
        ),
        Scenario(
            'Multiplying two positive numbers',
            Given('a_multiplication_function'),
            When('we_call_it_with_two_positive_numbers'),
            Then('we_will_get_a_positive_number')
        ),
        Scenario(
            'Multiplying two negative numbers',
            Given('a_multiplication_function'),
            When('we_call_it_with_two_negative_numbers'),
            Then('we_will_get_a_positive_number')
        )
    ),
    Feature(
        'Arithmetic Two',
        Scenario(
            'Adding two negative numbers',
            Given('an_adding_function'),
            When('we_call_it_with_two_negative_numbers'),
            Then('we_will_get_a_negative_number')
        ),
        Scenario(
            'Adding two positive numbers',
            Given('an_adding_function'),
            When('we_call_it_with_two_positive_numbers'),
            Then('we_will_get_a_negative_number')
        ),
        Scenario(
            'Multiplying two strings',
            Given('a_multiplication_function'),
            When('we_call_it_with_two_strings'),
            Then('a_typeerror_will_occur')
        ),
        Scenario(
            'Multiplying two positive numbers',
            Given('a_multiplication_function'),
            When('we_raise_an_exception'),
            Then('we_will_get_a_positive_number')
        ),
        Scenario(
            'An exception is raised',
            Given('an_exception'),
            When('we_call_it_with_two_positive_numbers'),
            Then('we_will_get_a_positive_number')
        )
    ),
    Feature(
        'Arithmetic Three',
        Scenario(
            'Adding two negative numbers',
            Given('an_adding_function'),
            When('we_call_it_with_two_negative_numbers'),
            Then('we_will_get_a_negative_number')
        ),
        Scenario(
            'Adding two positive numbers',
            Given('an_adding_function'),
            When('we_call_it_with_two_positive_numbers'),
            Then('we_will_get_a_positive_number')
        ),
        Scenario(
            'Multiplying two strings',
            Given('a_multiplication_function'),
            When('we_call_it_with_two_strings'),
            Then('a_typeerror_will_occur')
        ),
        Scenario(
            'Multiplying two positive numbers',
            Given('a_multiplication_function'),
            When('we_call_it_with_two_positive_numbers'),
            Then('we_will_get_a_positive_number')
        ),
        Scenario(
            'Multiplying two negative numbers',
            Given('a_multiplication_function'),
            When('we_call_it_with_two_negative_numbers'),
            Then('we_will_get_a_positive_number')
        )
    )
)
suite.run()
print(suite)



