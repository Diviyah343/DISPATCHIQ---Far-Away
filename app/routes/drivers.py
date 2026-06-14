from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.driver import Driver
from app.services.redis_service import publish_location, cache_driver_location, get_cached_driver_location
from pydantic import BaseModel

router = APIRouter(prefix="/drivers", tags=["drivers"])

class DriverCreate(BaseModel):
    name: str
    phone: str

class LocationUpdate(BaseModel):
    latitude: float
    longitude: float

@router.post("/register")
def register_driver(driver: DriverCreate, db: Session = Depends(get_db)):
    existing = db.query(Driver).filter(Driver.phone == driver.phone).first()
    if existing:
        raise HTTPException(status_code=400, detail="Phone number already registered")
    new_driver = Driver(name=driver.name, phone=driver.phone)
    db.add(new_driver)
    db.commit()
    db.refresh(new_driver)
    return new_driver

@router.put("/{driver_id}/location")
def update_location(driver_id: int, location: LocationUpdate, db: Session = Depends(get_db)):
    driver = db.query(Driver).filter(Driver.id == driver_id).first()
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    driver.latitude = location.latitude
    driver.longitude = location.longitude
    db.commit()
    db.refresh(driver)
    publish_location(driver_id, location.latitude, location.longitude)
    cache_driver_location(driver_id, location.latitude, location.longitude)
    return driver

@router.get("/available")
def get_available_drivers(db: Session = Depends(get_db)):
    drivers = db.query(Driver).filter(Driver.is_available == True).all()
    return drivers

@router.get("/{driver_id}/cached-location")
def get_driver_cached_location(driver_id: int):
    location = get_cached_driver_location(driver_id)
    if not location:
        raise HTTPException(status_code=404, detail="No cached location found")
    return location

@router.get("/{driver_id}")
def get_driver(driver_id: int, db: Session = Depends(get_db)):
    driver = db.query(Driver).filter(Driver.id == driver_id).first()
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    return driver