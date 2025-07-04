"""
End-to-end API tests using FastAPI's TestClient.
"""

import time

from fastapi.testclient import TestClient
            
from robot_control.app.main import app

client = TestClient(app)


def test_create_and_get_plan():
    req_payload = {
        "name": "sample-plan",
        "wall_width": 1.0,
        "wall_height": 1.0,
        "obstacles": [[0.25, 0.25, 0.25, 0.25]],
        "step_size": 0.1,
    }

    # Measure response time for creation
    start = time.perf_counter()
    create_resp = client.post("/plan", json=req_payload)
    elapsed_ms = (time.perf_counter() - start) * 1000

    assert create_resp.status_code == 200
    data = create_resp.json()
    assert "id" in data
    plan_id = data["id"]
    assert isinstance(plan_id, int)

    # Reasonable threshold: 200ms for local SQLite
    assert elapsed_ms < 200

    # Retrieve the created plan
    get_resp = client.get(f"/plan/{plan_id}")
    assert get_resp.status_code == 200
    plan_data = get_resp.json()

    assert plan_data["id"] == plan_id
    assert plan_data["name"] == req_payload["name"]

    points = plan_data["points"]
    assert points, "Points list should not be empty"

    # Ensure ordering by seq
    seqs = [p["seq"] for p in points]
    assert seqs == sorted(seqs), "Points must be ordered by seq"

    # Ensure no duplicate sequences
    assert len(seqs) == len(set(seqs)) 