from termcolor import colored
import textwrap
import traceback


def cyan(text):
    return colored(text, 'cyan')


def magenta(text):
    return colored(text, 'magenta')


def yellow(text):
    return colored(text, 'yellow')


def red(text):
    return colored(text, 'red')


def grey(text):
    return colored(text, 'white')


def extract_traceback(exception):
    return ''.join(traceback.format_tb(exception.__traceback__))


def indent(text, amount):
    return textwrap.indent(text, ' ' * amount)
