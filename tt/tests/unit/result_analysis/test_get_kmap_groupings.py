"""Test ``get_kmap_groupings``."""

import unittest

from tt.bittools import is_pow2
from tt.result_analysis import get_kmap_groupings
from tt.tests.factory import kmap_grid_factory
from tt.utils import init_2d_list


class TestGetKmapGroupings(unittest.TestCase):

    def helper_test_valid_groupings(self, value_grid):
        """Helper for asserting all went well in ``get_kmap_groupings``.

        Assert all dimensions of returned groupings are powers of 2 and that
        all values in the passed ``value_grid`` are covered by the returned
        lists of groups.

        """
        result_grid = init_2d_list(len(value_grid[0]),
                                   len(value_grid),
                                   init_val=0)
        kmap_grid = kmap_grid_factory(value_grid)
        groups = get_kmap_groupings(kmap_grid)

        for group in groups:
            # make sure all dimensions of groups are a power of 2
            self.assertTrue(is_pow2(group.h) and is_pow2(group.w),
                            msg='Non-pow2 dimension(s): '+str(group))

            # make sure all values are covered in the original grid
            for point in group.point_list:
                result_grid[point[0]][point[1]] = 1

        self.assertEqual(value_grid, result_grid)

    def test_empty_2_by_2(self):
        self.helper_test_valid_groupings(
            [
                [0, 0],
                [0, 0]
            ])

    def test_filled_2_by_2(self):
        self.helper_test_valid_groupings(
            [
                [1, 1],
                [1, 1]
            ])

    def test_odd_2_by_2(self):
        self.helper_test_valid_groupings(
            [
                [1, 0],
                [1, 1]
            ])

    def test_individual_2_by_2(self):
        self.helper_test_valid_groupings(
            [
                [1, 0],
                [0, 1]
            ])

    def test_odd_height_even_width_diff_pow2_by_1(self):
        # Assert that a height only 1 away from the closest power of 2, which
        # in this case is 5-4=1 does not affect the logic used in partitioning
        # the groups.
        self.helper_test_valid_groupings(
            [
                [1, 1, 1, 1, 0, 0, 0, 0],
                [1, 1, 1, 1, 0, 0, 0, 0],
                [1, 1, 1, 1, 0, 0, 0, 0],
                [1, 1, 1, 1, 0, 0, 0, 0],
                [1, 1, 1, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
            ])

    def test_odd_height_even_width_diff_pow2_gt_1(self):
        # Assert that a height greater than 1 away from the closest power of,
        # which in this case is 7-4=3 does not break the logic used in
        # partitioning the groups.
        self.helper_test_valid_groupings(
            [
                [1, 1, 1, 1, 0, 0, 0, 0],
                [1, 1, 1, 1, 0, 0, 0, 0],
                [1, 1, 1, 1, 0, 0, 0, 0],
                [1, 1, 1, 1, 0, 0, 0, 0],
                [1, 1, 1, 1, 0, 0, 0, 0],
                [1, 1, 1, 1, 0, 0, 0, 0],
                [1, 1, 1, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
            ])

    def test_even_height_odd_width_diff_pow2_by_1(self):
        self.helper_test_valid_groupings(
            [
                [0, 0, 0, 0],
                [0, 1, 1, 1],
                [0, 1, 1, 1],
                [0, 0, 0, 0]
            ])

    def test_even_height_odd_width_diff_pow2_by_gt_1(self):
        self.helper_test_valid_groupings(
            [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ])

    def test_odd_height_diff_pow2_by_1_odd_width_diff_pow2_by_1(self):
        self.helper_test_valid_groupings(
            [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 1, 1, 0, 0, 0],
                [0, 0, 1, 1, 1, 0, 0, 0],
                [0, 0, 1, 1, 1, 0, 0, 0],
                [0, 0, 1, 1, 1, 0, 0, 0],
                [0, 0, 1, 1, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
            ])

    def test_odd_height_diff_pow2_gt_1_odd_width_diff_pow2_by_1(self):
        self.helper_test_valid_groupings(
            [
                [0, 0, 1, 1, 1, 1, 1, 0],
                [0, 0, 1, 1, 1, 1, 1, 0],
                [0, 0, 1, 1, 1, 1, 1, 0],
                [0, 0, 1, 1, 1, 1, 1, 0],
                [0, 0, 1, 1, 1, 1, 1, 0],
                [0, 0, 1, 1, 1, 1, 1, 0],
                [0, 0, 1, 1, 1, 1, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
            ])

    def test_odd_height_diff_pow2_by_1_odd_width_diff_pow2_gt_1(self):
        self.helper_test_valid_groupings(
            [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 1, 1, 1, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
            ])

    def test_off_height_diff_pow2_gt_1_odd_width_diff_pow2_gt_1(self):
        self.helper_test_valid_groupings(
            [
                [1, 1, 1, 1, 1, 1, 1, 0],
                [1, 1, 1, 1, 1, 1, 1, 0],
                [1, 1, 1, 1, 1, 1, 1, 0],
                [1, 1, 1, 1, 1, 1, 1, 0],
                [1, 1, 1, 1, 1, 1, 1, 0],
                [1, 1, 1, 1, 1, 1, 1, 0],
                [1, 1, 1, 1, 1, 1, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
            ])

    def test_disjoint_simple(self):
        self.helper_test_valid_groupings(
            [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 1, 0, 0, 0, 0],
                [0, 0, 1, 1, 0, 0, 0, 0],
                [0, 0, 0, 1, 1, 1, 1, 0],
                [0, 0, 0, 0, 1, 1, 1, 0],
                [0, 0, 0, 0, 1, 1, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
            ])

    def test_scattered_1_by_1(self):
        self.helper_test_valid_groupings(
            [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                [0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ]
        )
