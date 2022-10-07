import sys

FIND_IN_ARRAY = '0'


def found_zero_position(array: str | int) -> None:
    zero_position = str(array).find(FIND_IN_ARRAY)
    if zero_position == -1:
        sys.stdout.write('Array does not contain zeros.')
    else:
        sys.stdout.write(
            f'The first zero will find on the position: {zero_position}.'
        )
