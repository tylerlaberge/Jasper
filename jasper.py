class Expect(object):

    def __init__(self, expected_data):
        self.expected_data = expected_data

    def to_be(self, actual_data):
        try:
            assert self.expected_data is actual_data
        except AssertionError:
            print(f"FAILURE: Expected {self.expected_data} to be {actual_data}")
            raise AssertionError()

    def to_equal(self, actual_data):
        try:
            assert self.expected_data == actual_data
        except AssertionError:
            print(f"FAILURE: Expected {self.expected_data} to equal {actual_data}")
            raise AssertionError()


class My(object):

    def __init__(self):
        self.elements = {}

    def __call__(self, *get_element_name, **set_elements_args):
        if get_element_name and set_elements_args:
            raise ValueError("Cannot call My object with both get and set args")
        elif get_element_name:
            if len(get_element_name) > 1:
                raise ValueError("Cannot get more than one element at a time")
            else:
                try:
                    return self.elements[get_element_name[0]]
                except KeyError:
                    raise ValueError("No element by that name in My object")
        elif set_elements_args:
            for key, value in set_elements_args.items():
                self.elements[key] = value

    def __str__(self):
        return f'My({self.elements})'


from functools import wraps


def feature(func):
    @wraps(func)
    def wrapper():
        wrapper.my = My()
        return func()

    return wrapper


def scenario(func):
    @wraps(func)
    def wrapper(my_feature):
        wrapper.my = My()
        wrapper.my(**my_feature.elements)
        return func()

    return wrapper


def given(func):
    @wraps(func)
    def wrapper(my):
        return func(my)
    return wrapper


def it(func):
    @wraps(func)
    def wrapper(my):
        return func(my)
    return wrapper


@feature
def some_feature():

    @given
    def foo(my):
        my(foo='foo')
        print(f"given foo function: {my}")

    @scenario
    def some_scenario():

        @given
        def bar(my):
            my(bar='bar')
            print(f"given bar function: {my}")

        @it
        def combines_foo_and_bar_into_foobar(my):
            print(f"it combines function: {my}")
            Expect(my('foo') + my('bar')).to_equal('foobar')

        bar(some_scenario.my)
        combines_foo_and_bar_into_foobar(some_scenario.my)
        print(f"some_scenario function: {some_scenario.my}")

    print(locals())
    foo(some_feature.my)
    some_scenario(some_feature.my)
    print(f"some_feature function: {some_feature.my}")


some_feature()

