from termcolor import colored
import textwrap
import traceback


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


def relevant_trace(exception):
    trace = traceback.format_tb(exception.__traceback__)
    relevant_traceback = trace[len(trace) - 2].split('\n')
    for index, line in enumerate(relevant_traceback):
        relevant_traceback[index] = line.strip()

    return relevant_traceback
