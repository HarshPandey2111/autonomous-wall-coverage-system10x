"""
CRUD helpers that sit between the FastAPI layer and the database.
"""

from sqlalchemy.orm import Session

from . import coverage, models, schemas


def create_plan(db: Session, req: schemas.PlanRequest) -> int:
    """Creates a new plan, stores it, and returns its ID."""
    points = coverage.generate_coverage(
        wall_width=req.wall_width,
        wall_height=req.wall_height,
        obstacles=req.obstacles,
        step_size=req.step_size,
    )

    traj = models.Trajectory(name=req.name)
    db.add(traj)
    db.commit()
    db.refresh(traj)

    db_points = [
        models.TrajectoryPoint(traj_id=traj.id, seq=idx, x=x, y=y)
        for idx, (x, y) in enumerate(points)
    ]
    db.bulk_save_objects(db_points)
    db.commit()

    return traj.id


def get_plan(db: Session, plan_id: int):
    """Retrieve a plan and its points from the database."""
    traj = db.query(models.Trajectory).filter(models.Trajectory.id == plan_id).first()
    if traj is None:
        return None

    points = (
        db.query(models.TrajectoryPoint)
        .filter(models.TrajectoryPoint.traj_id == plan_id)
        .order_by(models.TrajectoryPoint.seq)
        .all()
    )
    return traj, points 