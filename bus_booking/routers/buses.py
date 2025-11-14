# routers/buses.py
from fastapi import APIRouter, Depends, status, Query
from config.database import database
from services.bus_service import BusService
from schemas.bus import (
    BusCreate, BusUpdate, BusResponse, BookingCreate, 
    BookingResponse, SearchBuses
)

# Create router
router = APIRouter(prefix="/buses", tags=["buses"])

def get_bus_service():
    """Dependency injection for bus service"""
    return BusService(database)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_bus(
    bus: BusCreate,
    bus_service: BusService = Depends(get_bus_service)
):
    """Create a new bus"""
    return bus_service.create_bus(bus)

@router.get("/", response_model=list[BusResponse])
async def get_all_buses(
    bus_service: BusService = Depends(get_bus_service)
):
    """Get all buses"""
    return bus_service.get_all_buses()

@router.get("/search", response_model=list[BusResponse]) #path parameter
async def search_buses(
    source: str = Query(..., description="Source city"),
    destination: str = Query(..., description="Destination city"),
    travel_date: str = Query(..., description="Travel date (YYYY-MM-DD)"),
    bus_service: BusService = Depends(get_bus_service)
):
    """Search buses by route and date"""
    search_data = SearchBuses(
        source=source,
        destination=destination,
        travel_date=travel_date
    )
    return bus_service.search_buses(search_data)

@router.get("/{bus_id}", response_model=BusResponse) #query parameter
async def get_bus(
    bus_id: str,
    bus_service: BusService = Depends(get_bus_service)
):
    """Get a single bus by ID"""
    return bus_service.get_bus(bus_id)

@router.put("/{bus_id}")
async def update_bus(
    bus_id: str,
    bus_update: BusUpdate,
    bus_service: BusService = Depends(get_bus_service)
):
    """Update a bus"""
    return bus_service.update_bus(bus_id, bus_update)

@router.delete("/{bus_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_bus(
    bus_id: str,
    bus_service: BusService = Depends(get_bus_service)
):
    """Delete a bus"""
    return bus_service.delete_bus(bus_id)

@router.post("/{bus_id}/book", response_model=BookingResponse)
async def book_tickets(
    booking: BookingCreate,
    bus_service: BusService = Depends(get_bus_service)
):
    """Book tickets on a bus"""
    return bus_service.book_tickets(booking)