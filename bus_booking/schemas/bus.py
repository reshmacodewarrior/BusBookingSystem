# schemas/bus.py
from pydantic import BaseModel, Field, EmailStr #
from typing import Optional, List
from datetime import datetime
from enum import Enum

class BusType(str, Enum): #
    AC = "ac"
    NON_AC = "non_ac"
    SLEEPER = "sleeper"
    SEMI_SLEEPER = "semi_sleeper"

class SeatStatus(str, Enum):
    AVAILABLE = "available"
    BOOKED = "booked"
    RESERVED = "reserved"

class SeatBase(BaseModel):
    seat_number: str = Field(..., example="A1")
    seat_type: str = Field(..., example="window")
    price: float = Field(..., gt=0, example=500.0)

class SeatCreate(SeatBase):
    status: SeatStatus = SeatStatus.AVAILABLE

class SeatResponse(SeatBase):
    status: SeatStatus
    passenger_name: Optional[str] = None
    passenger_email: Optional[str] = None

class BusBase(BaseModel):
    bus_number: str = Field(..., min_length=3, max_length=20, example="BUS001")
    bus_name: str = Field(..., min_length=2, max_length=50, example="Express Travels")
    bus_type: BusType
    source: str = Field(..., min_length=2, max_length=50, example="New York")
    destination: str = Field(..., min_length=2, max_length=50, example="Boston")
    departure_time: datetime
    arrival_time: datetime
    total_seats: int = Field(..., gt=0, le=100, example=40)

class BusCreate(BusBase):
    seats: List[SeatCreate] = []

class BusUpdate(BaseModel):
    bus_name: Optional[str] = None
    bus_type: Optional[BusType] = None
    source: Optional[str] = None
    destination: Optional[str] = None
    departure_time: Optional[datetime] = None
    arrival_time: Optional[datetime] = None

class BusResponse(BusBase):
    id: str
    available_seats: int
    booked_seats: int
    seats: List[SeatResponse]
    created_at: datetime

class BookingCreate(BaseModel):
    bus_id: str = Field(..., example="507f1f77bcf86cd799439011")
    seat_numbers: List[str] = Field(..., example=["A1", "A2"])
    passenger_name: str = Field(..., min_length=2, max_length=50, example="John Doe")
    passenger_email: EmailStr = Field(..., example="john@example.com")
    passenger_phone: str = Field(..., min_length=10, max_length=15, example="+1234567890")

class BookingResponse(BaseModel):
    booking_id: str
    bus_id: str
    bus_number: str
    source: str
    destination: str
    departure_time: datetime
    seat_numbers: List[str]
    passenger_name: str
    passenger_email: str
    passenger_phone: str
    total_amount: float
    booking_status: str
    booked_at: datetime

class SearchBuses(BaseModel):
    source: str
    destination: str
    travel_date: str  # YYYY-MM-DD format