import math
from sqlalchemy.orm import Session
from app.models.driver import Driver
from app.models.order import Order

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    return R * c

def assign_nearest_driver(order: Order, db: Session) -> Driver | None:
    available_drivers = db.query(Driver).filter(
        Driver.is_available == True,
        Driver.latitude != None,
        Driver.longitude != None
    ).all()

    if not available_drivers:
        return None

    nearest_driver = None
    min_distance = float('inf')

    for driver in available_drivers:
        distance = haversine_distance(
            order.pickup_lat, order.pickup_lng,
            driver.latitude, driver.longitude
        )
        if distance < min_distance:
            min_distance = distance
            nearest_driver = driver

    if nearest_driver:
        nearest_driver.is_available = False
        order.driver_id = nearest_driver.id
        order.status = "assigned"
        db.commit()

    return nearest_driver