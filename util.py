""" Utility functions for Marvin. """

from collections import OrderedDict

ROMAN_NUMERAL_DICT = OrderedDict([
    (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'), (100, 'C'), (90, 'XC'),
    (50, 'L'), (40, 'XL'), (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')
    ])

def to_roman(n):
    """ Given int between 1 and 4000 returns corresponding Roman numeral. """
    if not 1 <= n <= 4000:
        raise ValueError('to_roman can only convert integers between 1 and '
                         '3999')
    result = ""
    for roman_value in ROMAN_NUMERAL_DICT.keys():
        how_many, remainder = divmod(n, roman_value)
        result += ROMAN_NUMERAL_DICT[roman_value] * how_many
        n = remainder
    return result
