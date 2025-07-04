"""
SQLAlchemy data models and database setup for the wall-finishing robot control system.
"""

from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Index, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

DATABASE_URL = "sqlite:///./robot.db"

# The SQLite 'check_same_thread=False' flag allows the connection to be shared across threads,
# which is useful during testing and in the FastAPI development server.
engine = create_engine(
    DATABASE_URL, echo=False, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Trajectory(Base):
    """
    Stores high-level metadata for a generated trajectory.
    """

    __tablename__ = "trajectories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Establish bidirectional relationship to points
    points = relationship(
        "TrajectoryPoint",
        back_populates="trajectory",
        cascade="all, delete-orphan",
        order_by="TrajectoryPoint.seq",
    )


class TrajectoryPoint(Base):
    """
    Represents an individual point in a trajectory.
    """

    __tablename__ = "trajectory_points"

    id = Column(Integer, primary_key=True, index=True)
    traj_id = Column(
        Integer, ForeignKey("trajectories.id", ondelete="CASCADE"), nullable=False, index=True
    )
    seq = Column(Integer, nullable=False)  # Order of the point in the trajectory
    x = Column(Float, nullable=False)
    y = Column(Float, nullable=False)

    trajectory = relationship("Trajectory", back_populates="points")

    # Composite index for fast ordered look-ups
    __table_args__ = (Index("idx_traj_seq", "traj_id", "seq"),)


# Create all tables on import.
Base.metadata.create_all(bind=engine) 