"""
Pydantic request/response schemas shared by the API.
"""

from typing import List, Tuple

from pydantic import BaseModel, Field


class PlanRequest(BaseModel):
    """
    Request payload for a new coverage plan.
    """

    name: str = Field(..., description="Human-readable name for the plan")
    wall_width: float = Field(..., gt=0, description="Width of the wall in metres")
    wall_height: float = Field(..., gt=0, description="Height of the wall in metres")
    obstacles: List[Tuple[float, float, float, float]] = Field(
        default_factory=list,
        description="List of rectangular obstacles as (x, y, width, height)",
    )
    step_size: float = Field(
        0.1,
        gt=0,
        description="Step size in metres between coverage points (defaults to 0.1)",
    )


class Point(BaseModel):
    """
    A single point in a trajectory.
    """

    seq: int
    x: float
    y: float


class PlanResponse(BaseModel):
    """
    Response payload for a stored plan.
    """

    id: int
    name: str
    points: List[Point] 