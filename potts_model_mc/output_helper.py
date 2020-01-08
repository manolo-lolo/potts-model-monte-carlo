from config import VERBOSE


def print_if_verbose(*args):
    if VERBOSE:
        print(*args)
