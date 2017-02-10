from jasper import given


@given
def a_dictionary_of_data(context):
    context.object = {
        'foo': 'bar',
        'foobar': {
            'bar': 'foo',
        }
    }
