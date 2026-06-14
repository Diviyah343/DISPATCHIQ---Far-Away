# DispatchIQ — Real-Time Logistics Dispatch Platform

> Smarter Deliveries, Faster Every Time

DispatchIQ is a real-time logistics dispatch platform that automatically assigns 
the nearest available driver to incoming orders using Haversine distance matching, 
provides live order tracking for customers, and gives operations teams full fleet 
visibility from a single dashboard.

Built for FAR AWAY 2026 — Logistics & Transit theme.

---

## Features

- **Intelligent Auto-Assignment** — Haversine-based nearest driver matching on every new order
- **Three-Portal System** — Customer portal, Driver portal, Operations dashboard
- **Event-Driven Architecture** — Redis pub/sub for real-time order and driver state updates
- **Live Map** — Leaflet + OpenStreetMap renders driver, pickup, and delivery positions
- **WebSocket Support** — Per-order and per-driver WebSocket channels built into the backend
- **Driver Location Caching** — Redis hash with 300s TTL for sub-millisecond dispatch lookups
- **Full Order Lifecycle** — Pending → Assigned → In Transit → Delivered

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI (Python, async) |
| Database | SQLAlchemy + SQLite |
| Real-time | Redis Pub/Sub + WebSockets |
| Location Cache | Redis Hash (300s TTL) |
| Frontend | Vanilla JS + HTML/CSS |
| Maps | Leaflet + OpenStreetMap |
| Server | Uvicorn (ASGI) |

---

## Getting Started

### Prerequisites

- Python 3.9+
- Redis server running locally

### Installation

```bash
git clone https://github.com/yourusername/dispatchiq.git
cd dispatchiq
pip install -r requirements.txt
```

### Environment Setup

Create a `.env` file in the root directory:

```env
DATABASE_URL=sqlite:///./dispatchiq.db
REDIS_URL=redis://localhost:6379
```

### Run

```bash
# Start Redis (if not already running)
redis-server

# Start the FastAPI server
uvicorn app.main:app --reload
```

Open `http://localhost:8000` in your browser.

---

## Project Structure
