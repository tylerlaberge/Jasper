from jasper import Context


class Given(object):

    def __init__(self, attribute_name, with_alias=None):
        name = with_alias or attribute_name
        self.context = Context({
            name: getattr(self, attribute_name)
        })

    def __call__(self, context):
        context.update(self.context)


