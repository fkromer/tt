"""A module used for transforming evaluation results into different forms."""

import itertools

from collections import namedtuple

from tt.bittools import (get_nth_gray_code, get_int_concatenation, is_pow2,
                         get_closest_smaller_pow2)
from tt.utils import init_2d_list


KmapPoint = namedtuple('KmapPoint', ['gray_code', 'val'])


class PointGroup(object):
    """Immutable, rectangular group of points represented as ``(r, c)`` tuples.

    Attributes:
        r (int): The zero-indexed, top-left-corner row of the rectangular
            group.
        c (int): The zero-indexed, top-left-corner column of the rectangular
            group.
        h (int): The height of the rectangular group.
        w (int): The width of the rectangular group.
        kmap_h (int): The height of the kmap containing this ``PointGroup``.
        kmap_w (int): The width of the kmap containing this ``PointGroup``.
        point_list (List[tuple(int, int)]): The list of points contained within
            this group, computed once at initilization.
        num_points (int): The length of ``point_list``.

    """

    def __init__(self, topleft_r_in, topleft_c_in, h_in, w_in,
                 kmap_h_in, kmap_w_in):
        self.r = topleft_r_in
        self.c = topleft_c_in
        self.h = h_in
        self.w = w_in
        self.kmap_h = kmap_h_in
        self.kmap_w = kmap_w_in
        self.point_list = self.gen_point_list()
        self.num_points = len(self.point_list)

    def __contains__(self, point_tuple):
        """__contains__ override.

        Args:
            point_typle (tuple(int, int)): A point of form ``(r, c)``.

        Returns:
            bool: Whether ``point_tuple`` is contained within this group.

        Notes:
            No type checking is done; if ``point_tuple`` is not of type
            ``tuple(int, int)`` then False is returned.

        """
        return point_tuple in self.point_list

    def __str__(self):
        """String representation of all points in this group."""
        return str(self.point_list)

    def gen_point_list(self):
        """Get list of all points in this group.

        Args:
            None.

        Returns:
            List[tuple(int, int)]: List of tuple of points contained within
                this group.

        Notes:
            Since ``PointGroup`` is meant to be immutable, this function
            should only be called once, at initilization.
        """
        return [(r, c)
                for r in range(self.r, self.r + self.h)
                for c in range(self.c, self.c + self.w)]

    def get_split_by_width(self, new_width):
        """TODO."""
        split_on_w = self.w - new_width
        group1 = PointGroup(self.r, self.c,
                            self.h, self.w - split_on_w,
                            self.kmap_h, self.kmap_w)
        group2 = PointGroup(self.r, self.c + split_on_w,
                            self.h, self.w - split_on_w,
                            self.kmap_h, self.kmap_w)
        return group1, group2

    def get_split_by_height(self, new_height):
        """TODO."""
        split_on_h = self.h - new_height
        group1 = PointGroup(self.r, self.c,
                            self.h - split_on_h, self.w,
                            self.kmap_h, self.kmap_w)
        group2 = PointGroup(self.r + split_on_h, self.c,
                            self.h - split_on_h, self.w,
                            self.kmap_h, self.kmap_w)
        return group1, group2


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
                                PointGroup(row - N, col, N + S + 1, width,
                                           h, w))
                        if nextN < N:
                            N = nextN
                        if nextS < S:
                            S = nextS
                    width += 1
                if S < maxS:
                    groups.append(
                        PointGroup(row - N, col, N + S + 1, width,
                                   h, w))
                maxS = 0

    # we now have rectangular groupings of the Kmap, but they are not
    # guaranteed to have power-of-2 dimensions (which is necessary for proper
    # optimization)
    pow2_partitioned_groups = []
    while groups:
        group = groups.pop()
        if not is_pow2(group.w):
            pow2_w = get_closest_smaller_pow2(group.w)
            new_group1, new_group2 = group.get_split_by_width(pow2_w)
            groups.append(new_group1)
            groups.append(new_group2)
            continue
        if not is_pow2(group.h):
            pow2_h = get_closest_smaller_pow2(group.h)
            new_group1, new_group2 = group.get_split_by_height(pow2_h)
            groups.append(new_group1)
            groups.append(new_group2)
            continue
        pow2_partitioned_groups.append(group)

    return pow2_partitioned_groups


def get_merged_wrapped_kmap_groups(kmap_group, point_group_list):
    """TODO."""
    candidate_merges = []  # list of pairs of possible groups to merge
    for group_pair in itertools.combinations(point_group_list):
        pass


def prune_kmap_groupings():
    """TODO."""
    pass


class TooFewKarnaughMapInputs(Exception):
    """Error for when a Karnaugh Map is attempted with less than 2 inputs.

    """

    pass
