# Robot Coverage Planner

A robust, database-driven control system for an autonomous wall-finishing robot. This project demonstrates intelligent path planning, efficient backend data management, and interactive 2D visualization—all built with modern Python technologies.

---

## 🚀 Overview

This system is designed to:
- **Compute optimal coverage paths** for rectangular walls, avoiding user-defined obstacles.
- **Store and retrieve trajectories** using a fast, indexed SQLite database.
- **Expose a clean API** for plan creation and retrieval (FastAPI).
- **Visualize robot paths** interactively in the browser (HTML Canvas + JS).
- **Log and monitor** all API requests with response times.
- **Test all endpoints** for correctness and performance.

---

## 🏗️ Architecture & Components

```
robot_control/
│
├── app/
│   ├── main.py        # FastAPI app: API, middleware, static serving
│   ├── models.py      # SQLAlchemy ORM models & DB setup
│   ├── schemas.py     # Pydantic request/response validation
│   ├── crud.py        # DB operations (create/retrieve plans)
│   ├── coverage.py    # Lawn-mower path planning algorithm
│   └── static/
│       └── index.html # HTML+JS Canvas visualizer
│
├── tests/
│   └── test_api.py    # Automated API tests (pytest + FastAPI TestClient)
│
├── requirements.txt   # Python dependencies
└── README.md          # This file
```

---

## 🧠 Key Features

- **Lawn-mower Coverage Algorithm:**
  - Efficiently covers the entire wall, skipping rectangular obstacles.
  - User-configurable wall size, obstacles, and step size.
- **RESTful API:**
  - `POST /plan` — Create a new plan (inputs: wall, obstacles, step size).
  - `GET /plan/{id}` — Retrieve a plan and its trajectory points.
- **Database-Driven:**
  - All plans and points are stored in SQLite with fast indexed queries.
- **Detailed Logging:**
  - Every request logs path, status, and response time (ms).
- **Interactive Visualization:**
  - HTML Canvas animates the robot's path for any plan ID.
- **Automated Testing:**
  - End-to-end tests for plan creation, retrieval, and timing.

---

## 🛠️ Technologies Used

- **Python 3.10+**
- **FastAPI** — Modern, async web framework
- **SQLAlchemy** — ORM for SQLite
- **Pydantic** — Data validation
- **pytest** — Testing
- **HTML5 Canvas + JavaScript** — Visualization
- **Uvicorn** — ASGI server

---

## ⚙️ Setup & Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd robot_control
   ```
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the server** (from the project root)
   ```bash
   uvicorn app.main:app --reload
   ```
   - The API and frontend will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000)

4. **Run tests**
   ```bash
   pytest -q
   ```

---

## 🧩 How It Works

### 1. **Coverage Planning**
- Implements a "lawn-mower" (zig-zag) sweep algorithm in `coverage.py`.
- Skips user-defined rectangular obstacles.
- Returns an ordered list of (x, y) points for the robot to follow.

### 2. **Backend Data Management**
- **models.py:** Defines `Trajectory` (plan metadata) and `TrajectoryPoint` (each path point).
- **crud.py:** Handles plan creation and retrieval.
- **main.py:** Exposes `/plan` (POST) and `/plan/{id}` (GET) endpoints.
- **Logging:** Middleware logs every request's path, status, and response time.

### 3. **Frontend Visualization**
- **index.html:**
  - User enters a Plan ID and clicks "Load".
  - Fetches the plan from the backend and animates the path on a Canvas.

### 4. **Testing**
- **tests/test_api.py:**
  - Creates a plan, retrieves it, and checks correctness and performance.

---

## 📝 Example Usage

### **Create a Plan (API)**
```bash
curl -X POST "http://127.0.0.1:8000/plan" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "test-plan",
    "wall_width": 5.0,
    "wall_height": 5.0,
    "obstacles": [[1.0, 1.0, 0.5, 0.5]],
    "step_size": 0.1
  }'
```
- **Response:** `{ "id": 1 }`

### **Visualize a Plan**
- Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.
- Enter the returned Plan ID (e.g., `1`) and click "Load".
- Watch the robot's path animate on the Canvas.

---
## How Ui and Output Look Like
![image](https://github.com/user-attachments/assets/26050890-062c-4fa5-81ba-e8336d2761cf)


## 🗂️What I achieved 

- **Modular, scalable architecture**: Each concern (API, DB, logic, frontend, tests) is cleanly separated.
- **Efficient path planning**: The algorithm is robust, handles obstacles, and is easy to extend.
- **Production-ready API**: FastAPI + SQLAlchemy + Pydantic for speed, safety, and validation.
- **Logging and monitoring**: Every request is logged with timing for easy profiling.
- **Interactive visualization**: No external plotting libraries—just pure HTML5 Canvas and JS.
- **Testing**: End-to-end tests ensure reliability and performance.
- **Easy to extend**: Add real-time features, more complex obstacles, or advanced analytics as needed.

---

