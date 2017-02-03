from jasper import Context
from jasper.utility import cyan


class JasperGiven(object):

    def __init__(self, attribute_name, with_alias=None):
        self.name = with_alias or attribute_name
        self.context = Context({
            self.name: getattr(self, attribute_name)
        })

    def __call__(self, context):
        context.update(self.context)

    def __str__(self):
        return cyan(f"Given: {self.context[self.name].__name__}")
