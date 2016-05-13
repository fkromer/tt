"""A module for simple manipulation of bits.
"""
import math


def get_int_concatenation(int1, int2, int_size):
    """Get the concatenation of two ints.

    Args:
        int1 (int): The int that will be the leading bit sequence in the
            result.
        int2 (int): The int that will be the trailing bit sequence in the
            result.
        int_size (int): The length (as number of bits) of ``int1`` and
            ``int2``.

    Returns:
        int: The concatention of ``int1`` and ``int2``, treated as integers
            with bit length of ``int_size``.

    Notes:
        ``int_size`` is assumed to be greater than or equal to the position of
            the most significant non-zero bit in ``int2``.

    Examples:
    >>> x = get_int_concatentation(1, 2, 2)
    >>> bin(x)
    '0b110'
    >>> x = get_int_concatentation(1, 2, 3)
    >>> bin(x)
    '0b1010'

    """
    return (int1 << int_size) | int2


def get_nth_gray_code(n):
    """Get the nth gray code.

    Args:
        n (int): The n in nth gray code.

    Returns:
        int: The nth gray code.

    Examples:
    >>> get_nth_gray_code(0)
    0
    >>> get_nth_gray_code(1)
    1
    >>> get_nth_gray_code(2)
    3
    >>> get_nth_gray_code(3)
    2

    """
    return n ^ (n >> 1)


def is_pow2(x):
    """Returns if input is a power of 2.

    Args:
        x (int): The number to test.

    Returns:
        bool: True if ``x`` is a power of 2, otherwise False.

    Examples:
    >>> is_pow2(1)
    True
    >>> is_pow2(45)
    False
    >>> is_pow2(512)
    True

    """
    return bool(x) and not (x & (x - 1))


def get_closest_smaller_pow2(x):
    """Get the closest power of 2.

    Args:
        x (int): The reference number.

    Returns:
        int: The closest power of 2 less than or equal to ``x``.

    Examples:
    >>> get_closest_smaller_pow2(63)
    32
    >>> get_closest_smaller_pow2(64)
    64
    >>> get_closest_smaller_pow2(65)
    64
    >>> get_closest_smaller_pow2(129)
    128

    """
    # there' sprobably a better way of doing this
    return 2 ** int(math.log2(x))


def get_bit_string(n, num_chars=None):
    """Convert ``n`` to a binary string representation.

    Args:
        n (int):
        num_chars (int): The total number of chars the result should include.
            The result is zero-filled to reach this number if necessary.

    Returns:
        str: The binary representation of ``n``.

    Notes:
        ``num_chars`` is assumed to be greater than or equal to the position of
            the most significant non-zero bit in ``n``.

    """
    fmt_str = '{:0' + (str(num_chars) if num_chars is not None else '') + 'b}'
    return fmt_str.format(n)


# def get_parity(x):
#     """Get the bit parity of ``x``.

#     Notes:
#         Not currently used, but this may be useful in the future.

#     """
#     c = 0
#     while x:
#         c += 1
#         x &= x - 1
#     return c
