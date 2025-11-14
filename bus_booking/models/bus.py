# models/bus.py
import datetime
from typing import List
from bson import ObjectId
from fastapi import HTTPException, status
from schemas.bus import SeatStatus, BusType

class BusModel:
    def __init__(self, database):
        self.database = database
        self._collection = None
    
    @property
    def collection(self):
        """Lazy loading of collection"""
        if self._collection is None:
            self._collection = self.database.get_collection("buses")
        return self._collection
    
    def _check_connection(self):
        """Check if database is connected"""
        if self.collection is None:
            raise HTTPException(   #Http Exception Status Code Error Handling 
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database connection not available"
            )
    
    def create_bus(self, bus_data: dict):
        """Create a new bus document"""
        self._check_connection()
        
        # Generate seats if not provided
        if not bus_data.get("seats"):
            bus_data["seats"] = self._generate_seats(bus_data["total_seats"])
        
        bus_data["created_at"] = datetime.datetime.now()
        bus_data["available_seats"] = bus_data["total_seats"]
        bus_data["booked_seats"] = 0
        
        result = self.collection.insert_one(bus_data)
        return str(result.inserted_id)
    
    def _generate_seats(self, total_seats: int):
        """Generate seat layout for the bus"""
        seats = []
        rows = total_seats // 4
        seat_types = ["window", "aisle", "aisle", "window"]
        
        for row in range(1, rows + 1):
            for col in range(1, 5):
                seat_number = f"{chr(64 + row)}{col}"
                seats.append({
                    "seat_number": seat_number,
                    "seat_type": seat_types[col - 1],
                    "price": 500.0,
                    "status": SeatStatus.AVAILABLE,
                    "passenger_name": None,
                    "passenger_email": None
                })
        
        return seats
    
    def get_all_buses(self):
        """Get all buses"""
        self._check_connection()
        
        buses = list(self.collection.find())
        for bus in buses:
            bus["_id"] = str(bus["_id"])
        return buses
    
    def get_bus_by_id(self, bus_id: str):
        """Get a single bus by ID"""
        self._check_connection()
        
        try:
            bus = self.collection.find_one({"_id": ObjectId(bus_id)})
            if bus:
                bus["_id"] = str(bus["_id"])
            return bus
        except:
            return None
    
    def search_buses(self, source: str, destination: str, travel_date: str):
        """Search buses by route and date"""
        self._check_connection()
        
        try:
            # Convert string date to datetime range
            travel_datetime = datetime.datetime.strptime(travel_date, "%Y-%m-%d")
            next_day = travel_datetime + datetime.timedelta(days=1)
            
            query = {
                "source": {"$regex": f"^{source}$", "$options": "i"},
                "destination": {"$regex": f"^{destination}$", "$options": "i"},
                "departure_time": {
                    "$gte": travel_datetime,
                    "$lt": next_day
                }
            }
            
            buses = list(self.collection.find(query))
            for bus in buses:
                bus["_id"] = str(bus["_id"])
            return buses
        except Exception as e:
            print(f"Search error: {e}")
            return []
    
    def book_seats(self, bus_id: str, seat_numbers: List[str], passenger_data: dict):
        """Book seats on a bus"""
        self._check_connection()
        
        try:
            bus = self.collection.find_one({"_id": ObjectId(bus_id)})
            if not bus:
                return False, "Bus not found"
            
            # Check if seats are available
            for seat_number in seat_numbers:
                seat = next((s for s in bus["seats"] if s["seat_number"] == seat_number), None)
                if not seat:
                    return False, f"Seat {seat_number} not found"
                if seat["status"] != SeatStatus.AVAILABLE:
                    return False, f"Seat {seat_number} is not available"
            
            # Update seat status
            update_result = self.collection.update_one(
                {"_id": ObjectId(bus_id)},
                {
                    "$set": {
                        "seats.$[elem].status": SeatStatus.BOOKED,
                        "seats.$[elem].passenger_name": passenger_data["name"],
                        "seats.$[elem].passenger_email": passenger_data["email"],
                        "available_seats": bus["available_seats"] - len(seat_numbers),
                        "booked_seats": bus["booked_seats"] + len(seat_numbers)
                    }
                },
                array_filters=[{"elem.seat_number": {"$in": seat_numbers}}]
            )
            
            return update_result.modified_count > 0, "Booking successful"
        except Exception as e:
            return False, f"Booking error: {str(e)}"
    
    def update_bus(self, bus_id: str, update_data: dict):
        """Update a bus document"""
        self._check_connection()
        
        try:
            # Remove None values
            update_data = {k: v for k, v in update_data.items() if v is not None}
            
            if update_data:
                result = self.collection.update_one(
                    {"_id": ObjectId(bus_id)},
                    {"$set": update_data}
                )
                return result.modified_count > 0
            return False
        except:
            return False
    
    def delete_bus(self, bus_id: str):
        """Delete a bus document"""
        self._check_connection()
        
        try:
            result = self.collection.delete_one({"_id": ObjectId(bus_id)})
            return result.deleted_count > 0
        except:
            return False