"""
Simple 'lawn-mower' coverage algorithm.

Given wall dimensions and rectangular obstacles, the algorithm sweeps
row by row (similar to how a lawn-mower works) while skipping any points
that fall inside an obstacle.

Dashed representation:

0,0 ----------------> +x (width)
 |
 v
 +y (height)

The origin (0,0) is assumed to be the bottom-left corner of the wall.
"""

from typing import List, Tuple


def _point_in_obstacle(x: float, y: float, obstacles: List[Tuple[float, float, float, float]]) -> bool:
    """Returns True if the point (x, y) lies inside any of the provided obstacles."""
    for ox, oy, ow, oh in obstacles:
        if ox <= x <= ox + ow and oy <= y <= oy + oh:
            return True
    return False


def _frange(start: float, stop: float, step: float):
    """A float range generator that is inclusive of the *stop* value with a small epsilon."""
    epsilon = 1e-9
    while start <= stop + epsilon:
        yield round(start, 6)  # Rounding keeps the floats tidy
        start += step


def generate_coverage(
    wall_width: float,
    wall_height: float,
    obstacles: List[Tuple[float, float, float, float]],
    step_size: float,
):
    """
    Generates an ordered list of (x, y) points that cover the entire wall surface
    while avoiding all obstacle rectangles.

    Parameters
    ----------
    wall_width : float
        Width of the wall (metres).
    wall_height : float
        Height of the wall (metres).
    obstacles : List[Tuple[float, float, float, float]]
        Each obstacle is defined by (x, y, width, height) where (x, y) is the
        bottom-left corner.
    step_size : float
        Distance between consecutive points (metres).

    Returns
    -------
    List[Tuple[float, float]]
        Ordered list of (x, y) points.
    """
    if step_size <= 0:
        raise ValueError("step_size must be > 0")

    points: List[Tuple[float, float]] = []
    row_idx = 0
    y = 0.0

    # Sweep rows until we exceed the wall height
    while y <= wall_height + 1e-9:
        xs = list(_frange(0.0, wall_width, step_size))
        # Alternate sweep direction every row
        if row_idx % 2 == 1:
            xs.reverse()

        for x in xs:
            if not _point_in_obstacle(x, y, obstacles):
                points.append((x, y))

        y += step_size
        row_idx += 1

    return points 