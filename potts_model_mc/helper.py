from config import q, WIDTH, VERBOSE, TEMPERATURE, J, h, FIX_LEFT, FIX_TOP, FIX_RIGHT, FIX_BOTTOM


def print_if_verbose(*args):
    if VERBOSE:
        print(*args)


def check_config_valid():
    assert(q > 1)
    assert(WIDTH > 1)
    assert(0.01 < TEMPERATURE < 100)
    assert(0 <= J <= 100)
    assert(0 <= h <= 100)
    assert(FIX_LEFT is None or 0 < FIX_LEFT < q)
    assert(FIX_TOP is None or 0 < FIX_TOP < q)
    assert(FIX_RIGHT is None or 0 < FIX_RIGHT < q)
    assert(FIX_BOTTOM is None or 0 < FIX_BOTTOM < q)
