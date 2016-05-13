"""A module used for transforming evaluation results into different forms."""

from collections import namedtuple

from tt.bittools import (get_nth_gray_code, get_int_concatenation, is_pow2,
                         get_closest_smaller_pow2)
from tt.utils import init_2d_list


KmapPoint = namedtuple('KmapPoint', ['gray_code', 'val'])


class PointGroup(object):
    """TODO

    """

    def __init__(self, topleft_r_in, topleft_c_in, h_in, w_in):
        self.r = topleft_r_in
        self.c = topleft_c_in
        self.h = h_in
        self.w = w_in

    def get_point_list(self):
        return [(r, c)
                for r in range(self.r, self.r + self.h)
                for c in range(self.c, self.c + self.w)]

    def split_by_width(self, new_width):
        split_on_w = self.w - new_width
        group1 = PointGroup(self.r, self.c,
                            self.h, self.w - split_on_w)
        group2 = PointGroup(self.r, self.c + split_on_w,
                            self.h, self.w - split_on_w)
        return group1, group2

    def split_by_height(self, new_height):
        split_on_h = self.h - new_height
        group1 = PointGroup(self.r, self.c,
                            self.h - split_on_h, self.w)
        group2 = PointGroup(self.r + split_on_h, self.c,
                            self.h - split_on_h, self.w)
        return group1, group2

    def __str__(self):
        return str(self.get_point_list())


def to_sop_form(high_indices, symbol_list):
    pass


def to_pos_form(low_indices, symbol_list):
    pass


def to_minimal_form():
    pass


def eval_result_as_kmap_grid(eval_result):
    """Convert an ``EvaluationResultWrapper`` instance to a Karnuagh Map grid.

    Args:
        eval_result (EvaluationResultWrapper): The result instance which will
            be converted to a more intuitive representation of a Karnaugh Map.

    Returns:
        List[List[KmapPoint]]: A list array of ``KmapPoint``s, in row-by-row
            ordering according to increasing Gray Code.

    Raises:
        TooFewKarnaughMapInputs: Raise if less than 2 inputs are found in
            ``eval_result``.

    """
    num_vars = len(eval_result.input_symbols)

    if num_vars < 2:
        raise TooFewKarnaughMapInputs('Karnaugh Map generation requires an '
                                      'equation of at least 2 variables.')

    row_pow = num_vars // 2
    col_pow = row_pow + num_vars % 2

    num_rows = 2 ** row_pow
    num_cols = 2 ** col_pow

    kmap_grid = []

    col_gcodes = [get_nth_gray_code(n) for n in range(num_cols)]
    row_gcodes = col_gcodes[:num_rows]

    for i, row_gcode in enumerate(row_gcodes):
        kmap_grid.append([])
        for col_gcode in col_gcodes:
            gcode = get_int_concatenation(row_gcode, col_gcode, col_pow)
            kmap_point = KmapPoint(
                gray_code=gcode, val=eval_result.result_list[gcode])
            kmap_grid[i].append(kmap_point)

    return kmap_grid


def get_kmap_groupings(kmap_grid):
    """Get rectangular groups of high values in a Kmap grid.

    Uses the algorithm described at:
    http://www.montefiore.ulg.ac.be/~pierard/rectangles/

    """
    def kmap_val(r, c):
        return kmap_grid[r][c].val

    w = len(kmap_grid[0])
    h = len(kmap_grid)

    dN = init_2d_list(w, h)
    dS = init_2d_list(w, h)

    # groups are in format (top left row, top left col, width, height)
    groups = []

    # init dN
    for col in range(w):
        dN[0][col] = 0 if kmap_val(0, col) else -1

    for row in range(1, h):
        for col in range(w):
            if not kmap_val(row, col):
                dN[row][col] = -1
            else:
                dN[row][col] = dN[row - 1][col] + 1

    # init dS
    for col in range(w):
        dS[h - 1][col] = 0 if kmap_val(h - 1, col) else -1

    for row in range(h - 2, -1, -1):
        for col in range(w):
            if not kmap_val(row, col):
                dS[row][col] = -1
            else:
                dS[row][col] = dS[row + 1][col] + 1

    # main partitioning algorithm
    for col in range(w - 1, -1, -1):
        maxS = h
        for row in range(h - 1, -1, -1):
            maxS += 1
            if (kmap_val(row, col) and (
                    col == 0 or not kmap_val(row, col - 1))):
                N = dN[row][col]
                S = dS[row][col]
                width = 1
                while (col + width) < w and kmap_val(row, col + width):
                    nextN = dN[row][col + width]
                    nextS = dS[row][col + width]
                    if (nextN < N) or (nextS < S):
                        if S < maxS:
                            groups.append(
                                PointGroup(row - N, col, N + S + 1, width))
                        if nextN < N:
                            N = nextN
                        if nextS < S:
                            S = nextS
                    width += 1
                if S < maxS:
                    groups.append(
                        PointGroup(row - N, col, N + S + 1, width))
                maxS = 0

    # we now have rectangular groupings of the Kmap, but they are not
    # guaranteed to have power-of-2 dimensions (which is necessary for proper
    # optimization)
    pow2_partitioned_groups = []
    while groups:
        group = groups.pop()
        if not is_pow2(group.w):
            pow2_w = get_closest_smaller_pow2(group.w)
            new_group1, new_group2 = group.split_by_width(pow2_w)
            groups.append(new_group1)
            groups.append(new_group2)
            continue
        if not is_pow2(group.h):
            pow2_h = get_closest_smaller_pow2(group.h)
            new_group1, new_group2 = group.split_by_height(pow2_h)
            groups.append(new_group1)
            groups.append(new_group2)
            continue
        pow2_partitioned_groups.append(group)

    return pow2_partitioned_groups


def prune_kmap_groupings():
    """TODO.

    """
    pass


class ExpandedKmapGrid(object):
    """Wraps a 2-D list representation of Karnaugh Map.

    For the optimization of Karnaugh Map groupings.

    """

    def __init__(self, kmap):
        self.min_row = -len(kmap[0][0])
        self.min_col = 0
        self.max_row = -2 * self.min_row
        self.max_col = 0

    def get_val(r, c):
        pass


class TooFewKarnaughMapInputs(Exception):
    """Error for when a Karnaugh Map is attempted with less than 2 inputs.

    """

    pass
