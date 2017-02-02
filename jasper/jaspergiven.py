from jasper import Context


class JasperGiven(object):

    def __init__(self, attribute_name, with_alias=None):
        self.name = with_alias or attribute_name
        self.context = Context({
            self.name: getattr(self, attribute_name)
        })

    def __call__(self, context):
        context.update(self.context)

    def __str__(self):
        return f"Given: {self.context[self.name].__name__}"
