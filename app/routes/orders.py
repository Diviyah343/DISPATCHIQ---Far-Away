from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.order import Order
from app.models.driver import Driver
from app.services.dispatch import assign_nearest_driver
from app.services.redis_service import publish_order_status
from pydantic import BaseModel

router = APIRouter(prefix="/orders", tags=["orders"])

class OrderCreate(BaseModel):
    pickup_address: str
    delivery_address: str
    pickup_lat: float
    pickup_lng: float
    delivery_lat: float
    delivery_lng: float

class StatusUpdate(BaseModel):
    status: str

@router.post("/create")
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    new_order = Order(
        pickup_address=order.pickup_address,
        delivery_address=order.delivery_address,
        pickup_lat=order.pickup_lat,
        pickup_lng=order.pickup_lng,
        delivery_lat=order.delivery_lat,
        delivery_lng=order.delivery_lng,
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    assigned_driver = assign_nearest_driver(new_order, db)
    db.refresh(new_order)

    publish_order_status(new_order.id, new_order.status, new_order.driver_id)

    return {
        "order": new_order,
        "assigned_driver": {
            "id": assigned_driver.id,
            "name": assigned_driver.name,
            "phone": assigned_driver.phone
        } if assigned_driver else None
    }

@router.get("/all")
def get_all_orders(db: Session = Depends(get_db)):
    orders = db.query(Order).all()
    return orders

@router.get("/{order_id}")
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.put("/{order_id}/status")
def update_status(order_id: int, status_update: StatusUpdate, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    valid_statuses = ["pending", "assigned", "in_progress", "delivered"]
    if status_update.status not in valid_statuses:
        raise HTTPException(status_code=400, detail="Invalid status")

    order.status = status_update.status

    if status_update.status == "delivered" and order.driver_id:
        driver = db.query(Driver).filter(Driver.id == order.driver_id).first()
        if driver:
            driver.is_available = True

    db.commit()
    db.refresh(order)

    publish_order_status(order.id, order.status, order.driver_id)

    return order