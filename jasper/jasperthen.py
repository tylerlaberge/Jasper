class JasperThen(object):

    def __init__(self, function_name):
        self.then_function = getattr(self, function_name)

    def __call__(self, context):
        self.context = context
        self.then_function()
