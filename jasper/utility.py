from termcolor import colored


def cyan(text):
    return colored(text, 'cyan')


def red(text):
    return colored(text, 'red')


def extract_traceback(exception):
    return exception.__traceback__.tb_frame.f_code.co_filename, exception.__traceback__.tb_lineno