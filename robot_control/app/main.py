"""
FastAPI application serving the wall-finishing robot control API and static frontend.
"""

import time
from pathlib import Path
from typing import Generator

from fastapi import Depends, FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from starlette.status import HTTP_404_NOT_FOUND

from . import crud, models, schemas

app = FastAPI(title="Robot Coverage Planner")


# ------------------------ Database dependency ------------------------ #

def get_db() -> Generator:
    """Yields a SQLAlchemy session that is closed after the request."""
    db = models.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ------------------------ Middleware ------------------------ #


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.perf_counter()
    response: Response = await call_next(request)
    process_time = (time.perf_counter() - start_time) * 1000  # milliseconds
    print(
        f"{request.method} {request.url.path} - {response.status_code} ({process_time:.2f} ms)"
    )
    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------ Routes ------------------------ #


@app.post("/plan")
def create_plan(req: schemas.PlanRequest, db=Depends(get_db)):
    """Generate a new coverage plan and return its identifier."""
    plan_id = crud.create_plan(db, req)
    return {"id": plan_id}


@app.get("/plan/{plan_id}", response_model=schemas.PlanResponse)
def read_plan(plan_id: int, db=Depends(get_db)):
    """Retrieve a stored plan by ID."""
    result = crud.get_plan(db, plan_id)
    if result is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Plan not found.")

    traj, points = result
    return {
        "id": traj.id,
        "name": traj.name,
        "points": [{"seq": p.seq, "x": p.x, "y": p.y} for p in points],
    }


# ------------------------ Static frontend ------------------------ #

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/")
def serve_index():
    """Serve the HTML frontend residing in the static directory."""
    index_file = STATIC_DIR / "index.html"
    return FileResponse(index_file)


# ------------------------ Uvicorn entrypoint ------------------------ #

# This allows: `uvicorn robot_control.app.main:app --reload`
__all__: tuple[str, ...] = ("app",) 