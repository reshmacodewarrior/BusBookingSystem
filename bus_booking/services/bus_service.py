# services/bus_service.py
from fastapi import HTTPException, status
from models.bus import BusModel
from schemas.bus import (
    BusCreate, BusUpdate, BusResponse, BookingCreate, 
    BookingResponse, SearchBuses, SeatResponse
)
import datetime
from bson import ObjectId

class BusService:
    def __init__(self, database):
        self.database = database
        self.bus_model = BusModel(database)
    
    def create_bus(self, bus: BusCreate) -> dict:
        """Create a new bus"""
        bus_data = bus.dict()
        bus_id = self.bus_model.create_bus(bus_data)
        return {"message": "Bus created successfully", "id": bus_id}
    
    def get_all_buses(self) -> list:
        """Get all buses"""
        buses_data = self.bus_model.get_all_buses()
        
        buses_response = []
        for bus in buses_data:
            buses_response.append(self._convert_to_bus_response(bus))
        
        return buses_response
    
    def get_bus(self, bus_id: str) -> BusResponse:
        """Get a single bus by ID"""
        bus = self.bus_model.get_bus_by_id(bus_id)
        if not bus:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Bus with ID {bus_id} not found"
            )
        
        return self._convert_to_bus_response(bus)
    
    def search_buses(self, search: SearchBuses) -> list:
        """Search buses by route and date"""
        buses_data = self.bus_model.search_buses(
            search.source, 
            search.destination, 
            search.travel_date
        )
        
        buses_response = []
        for bus in buses_data:
            buses_response.append(self._convert_to_bus_response(bus))
        
        return buses_response
    
    def book_tickets(self, booking: BookingCreate) -> BookingResponse:
        """Book tickets on a bus"""
        passenger_data = {
            "name": booking.passenger_name,
            "email": booking.passenger_email
        }
        
        success, message = self.bus_model.book_seats(
            booking.bus_id, 
            booking.seat_numbers, 
            passenger_data
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=message
            )
        
        # Get bus details for response
        bus = self.bus_model.get_bus_by_id(booking.bus_id)
        total_amount = sum(
            seat["price"] for seat in bus["seats"] 
            if seat["seat_number"] in booking.seat_numbers
        )
        
        return BookingResponse(
            booking_id=str(ObjectId()),
            bus_id=booking.bus_id,
            bus_number=bus["bus_number"],
            source=bus["source"],
            destination=bus["destination"],
            departure_time=bus["departure_time"],
            seat_numbers=booking.seat_numbers,
            passenger_name=booking.passenger_name,
            passenger_email=booking.passenger_email,
            passenger_phone=booking.passenger_phone,
            total_amount=total_amount,
            booking_status="confirmed",
            booked_at=datetime.datetime.now()
        )
    
    def update_bus(self, bus_id: str, bus_update: BusUpdate) -> dict:
        """Update a bus"""
        success = self.bus_model.update_bus(bus_id, bus_update.dict(exclude_unset=True))
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No valid fields to update or bus not found"
            )
        
        return {"message": "Bus updated successfully"}
    
    def delete_bus(self, bus_id: str) -> dict:
        """Delete a bus"""
        success = self.bus_model.delete_bus(bus_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Bus with ID {bus_id} not found"
            )
        
        return {"message": "Bus deleted successfully"}
    
    def _convert_to_bus_response(self, bus_data: dict) -> BusResponse:
        """Convert MongoDB bus data to response schema"""
        seats_response = []
        for seat in bus_data.get("seats", []):
            seats_response.append(SeatResponse(
                seat_number=seat["seat_number"],
                seat_type=seat["seat_type"],
                price=seat["price"],
                status=seat["status"],
                passenger_name=seat.get("passenger_name"),
                passenger_email=seat.get("passenger_email")
            ))
        
        return BusResponse(
            id=bus_data["_id"],
            bus_number=bus_data["bus_number"],
            bus_name=bus_data["bus_name"],
            bus_type=bus_data["bus_type"],
            source=bus_data["source"],
            destination=bus_data["destination"],
            departure_time=bus_data["departure_time"],
            arrival_time=bus_data["arrival_time"],
            total_seats=bus_data["total_seats"],
            available_seats=bus_data.get("available_seats", 0),
            booked_seats=bus_data.get("booked_seats", 0),
            seats=seats_response,
            created_at=bus_data["created_at"]
        )