from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    pickup_address = Column(String, nullable=False)
    delivery_address = Column(String, nullable=False)
    pickup_lat = Column(Float, nullable=False)
    pickup_lng = Column(Float, nullable=False)
    delivery_lat = Column(Float, nullable=False)
    delivery_lng = Column(Float, nullable=False)
    status = Column(String, default="pending")  # pending, assigned, in_progress, delivered
    driver_id = Column(Integer, ForeignKey("drivers.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())