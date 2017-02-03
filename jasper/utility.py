from termcolor import colored
import textwrap


def cyan(text):
    return colored(text, 'cyan')


def red(text):
    return colored(text, 'red')


def grey(text):
    return colored(text, 'white')


def extract_traceback(exception):
    return exception.__traceback__.tb_frame.f_code.co_filename, exception.__traceback__.tb_lineno


def indent(text, amount):
    return textwrap.indent(text, ' ' * amount)
