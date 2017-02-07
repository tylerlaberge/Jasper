from termcolor import colored
import textwrap
import traceback
from collections import namedtuple


def dict_to_namedtuple(name, dictionary):
    return namedtuple(name, dictionary.keys())(**dictionary)


def blue(text):
    return colored(text, 'blue')


def magenta(text):
    return colored(text, 'magenta')


def yellow(text):
    return colored(text, 'yellow')


def cyan(text):
    return colored(text, 'cyan')


def red(text):
    return colored(text, 'red')


def grey(text):
    return colored(text, 'white')


def extract_traceback(exception):
    return ''.join(traceback.format_tb(exception.__traceback__))


def indent(text, amount):
    return textwrap.indent(text, ' ' * amount)
