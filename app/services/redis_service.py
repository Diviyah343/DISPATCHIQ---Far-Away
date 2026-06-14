import redis
import json
import os
from dotenv import load_dotenv

load_dotenv()

r = redis.Redis.from_url(os.getenv("REDIS_URL"), decode_responses=True, protocol=2)

def publish_location(driver_id: int, latitude: float, longitude: float):
    message = {
        "driver_id": driver_id,
        "latitude": latitude,
        "longitude": longitude
    }
    r.publish(f"driver_{driver_id}_location", json.dumps(message))

def publish_order_status(order_id: int, status: str, driver_id: int = None):
    message = {
        "order_id": order_id,
        "status": status,
        "driver_id": driver_id
    }
    r.publish(f"order_{order_id}_status", json.dumps(message))

def cache_driver_location(driver_id: int, latitude: float, longitude: float):
    r.hset(f"driver_{driver_id}", "latitude", latitude)
    r.hset(f"driver_{driver_id}", "longitude", longitude)
    r.expire(f"driver_{driver_id}", 300)

def get_cached_driver_location(driver_id: int):
    data = r.hgetall(f"driver_{driver_id}")
    if data:
        return {
            "latitude": float(data["latitude"]),
            "longitude": float(data["longitude"])
        }
    return None