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

