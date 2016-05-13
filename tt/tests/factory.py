"""Make data structures for testing on the fly."""

from tt.bittools import get_nth_gray_code
from tt.result_analysis import KmapPoint
from tt.utils import init_2d_list


def kmap_grid_factory(val_array):
    """Get a 2-D array of instances of KmapPoint, from a binary array.

    """
    num_cols = len(val_array[0])
    num_rows = len(val_array)
    the_grid = init_2d_list(num_cols, num_rows)

    for r in range(num_rows):
        for c in range(num_cols):
            the_grid[r][c] = KmapPoint(
                get_nth_gray_code(c + r * num_cols),
                val_array[r][c])

    return the_grid
