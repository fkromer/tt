"""Meta-data for tt boolean operations."""

import logging as log


# === Wrapper Classes =========================================================
class BooleanOperator(object):

    def __init__(self, precedence_in, bool_func_in, nice_name_in, *args):
        self.precedence = precedence_in
        self.bool_func = bool_func_in
        self.nice_name = nice_name_in
        self.equivalent_symbols = list(args)

    def result(self, a, b):
        return self.bool_func(a, b)

    def __str__(self):
        return self.nice_name + ' (' + ', '.join(self.equivalent_symbols) + ')'


# === Boolean Functions =======================================================
def tt_and(a, b):
    return int(a and b)


def tt_nand(a, b):
    return int(not(a and b))


def tt_or(a, b):
    return int(a or b)


def tt_nor(a, b):
    return int(not(a or b))


def tt_xor(a, b):
    return int(a != b)


def tt_xnor(a, b):
    return int(a == b)


def tt_uncallable(a, b):
    log.critical('Boolean not function was explicitly called. '
                 'This should not happen; not is implemented as xor with 1. '
                 'Cannot continue program execution.')
    raise RuntimeError


# === Schema Information ======================================================
precedence = {
    'ZERO': 0,
    'LOW': 1,
    'MEDIUM': 2,
    'HIGH': 3
}

SYM_NOT = '~'
SYM_XOR = '+'
SYM_XNOR = '@'
SYM_AND = '&'
SYM_NAND = '$'
SYM_OR = '|'
SYM_NOR = '%'

schema = {
    SYM_NOT: BooleanOperator(precedence['HIGH'],
                             tt_uncallable,
                             'not',
                             'not', 'NOT', '~', '!'),
    SYM_XOR: BooleanOperator(precedence['MEDIUM'],
                             tt_xor,
                             'xor',
                             'xor', 'XOR'),
    SYM_XNOR: BooleanOperator(precedence['MEDIUM'],
                              tt_xnor,
                              'xnor/iff',
                              'xnor', 'XNOR', 'nxor', 'NXOR', 'iff', '<->'),
    SYM_AND: BooleanOperator(precedence['LOW'],
                             tt_and,
                             'and',
                             'and', 'AND', '&&', '&', '/\\'),
    SYM_NAND: BooleanOperator(precedence['LOW'],
                              tt_nand,
                              'nand',
                              'nand', 'NAND'),
    SYM_OR: BooleanOperator(precedence['ZERO'],
                            tt_or,
                            'or',
                            'or', 'OR', '||', '|', '\\/'),
    SYM_NOR: BooleanOperator(precedence['ZERO'],
                             tt_nor,
                             'nor',
                             'nor', 'NOR')
}

schema_search_ordered_list = [SYM_XNOR,
                              SYM_XOR,
                              SYM_NOR,
                              SYM_NAND,
                              SYM_AND,
                              SYM_OR,
                              SYM_NOT]
