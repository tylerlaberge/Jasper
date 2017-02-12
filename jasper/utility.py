import traceback


def extract_traceback(exception):
    return ''.join(traceback.format_tb(exception.__traceback__))



