# 🚌 Bus Ticket Booking System - FastAPI

A complete, production-ready bus ticket booking system built with FastAPI, MongoDB, and modern Python practices. Perfect for teaching FastAPI concepts to junior developers.

## 📋 Table of Contents
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [API Endpoints](#api-endpoints)
- [FastAPI Concepts Covered](#fastapi-concepts-covered)
- [Database Schema](#database-schema)
- [Testing](#testing)
- [Deployment](#deployment)
- [Teaching Guide](#teaching-guide)

## ✨ Features

- **Bus Management**: Full CRUD operations for buses
- **Seat Booking**: Real-time seat availability and booking
- **Search System**: Find buses by route and travel date
- **RESTful API**: Proper HTTP methods and status codes
- **Data Validation**: Comprehensive input validation with Pydantic
- **Error Handling**: Meaningful error messages and status codes
- **Auto Documentation**: Swagger UI and ReDoc included
- **Modular Architecture**: Clean separation of concerns

## 🏗️ Project Structure

```
bus_booking_api/
├── main.py                 # FastAPI application entry point
├── config/
│   ├── __init__.py
│   └── database.py         # MongoDB connection configuration
├── models/
│   ├── __init__.py
│   └── bus.py             # Database models and operations
├── schemas/
│   ├── __init__.py
│   └── bus.py             # Pydantic models for validation
├── services/
│   ├── __init__.py
│   └── bus_service.py     # Business logic layer
├── routers/
│   ├── __init__.py
│   └── buses.py           # API routes and endpoints
├── .env                   # Environment variables
└── requirements.txt       # Python dependencies
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- MongoDB (local or Atlas)
- pip (Python package manager)

### Step 1: Clone and Setup
```bash
# Create project directory
mkdir bus_booking_api
cd bus_booking_api

# Create virtual environment
python -m venv fastapi_env
source fastapi_env/bin/activate  # On Windows: fastapi_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Environment Configuration
Create `.env` file:
```env
MONGODB_URL=mongodb://localhost:27017/
DATABASE_NAME=bus_booking_system
```

### Step 3: Run the Application
```bash
uvicorn main:app --reload --port 8000
```

### Step 4: Access the Application
- **API**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📡 API Endpoints

### Bus Management
| Method | Endpoint | Description | Status Code |
|--------|----------|-------------|-------------|
| `POST` | `/buses/` | Create new bus | 201 Created |
| `GET` | `/buses/` | Get all buses | 200 OK |
| `GET` | `/buses/{id}` | Get bus by ID | 200 OK |
| `PUT` | `/buses/{id}` | Update bus | 200 OK |
| `DELETE` | `/buses/{id}` | Delete bus | 204 No Content |

### Search & Booking
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/buses/search?source=X&destination=Y&date=Z` | Search buses |
| `POST` | `/buses/{id}/book` | Book tickets |

### Example Requests

**Create Bus:**
```bash
curl -X POST "http://localhost:8000/buses/" \
-H "Content-Type: application/json" \
-d '{
  "bus_number": "BUS001",
  "bus_name": "Express Travels",
  "bus_type": "ac",
  "source": "New York",
  "destination": "Boston",
  "departure_time": "2024-01-15T08:00:00",
  "arrival_time": "2024-01-15T12:00:00",
  "total_seats": 40
}'
```

**Search Buses:**
```bash
curl "http://localhost:8000/buses/search?source=New%20York&destination=Boston&travel_date=2024-01-15"
```

**Book Tickets:**
```bash
curl -X POST "http://localhost:8000/buses/507f1f77bcf86cd799439011/book" \
-H "Content-Type: application/json" \
-d '{
  "seat_numbers": ["A1", "A2"],
  "passenger_name": "John Doe",
  "passenger_email": "john@example.com",
  "passenger_phone": "+1234567890"
}'
```

## 🎓 FastAPI Concepts Covered

### Core Concepts
- ✅ **Route Decorators** - `@app.get()`, `@app.post()`, etc.
- ✅ **Path Parameters** - Dynamic URL segments
- ✅ **Query Parameters** - URL query string parameters
- ✅ **Request Body** - JSON data parsing with Pydantic
- ✅ **Response Models** - Output validation and serialization
- ✅ **HTTP Status Codes** - Proper RESTful status codes
- ✅ **Error Handling** - HTTPException with custom messages
- ✅ **Dependency Injection** - Service layer pattern
- ✅ **API Router** - Modular route organization

### Advanced Features
- ✅ **Pydantic Models** - Data validation with type hints
- ✅ **Enum Types** - Predefined choice validation
- ✅ **Field Validation** - Constraints and custom validators
- ✅ **Automatic Documentation** - Swagger UI and ReDoc
- ✅ **Database Integration** - MongoDB with PyMongo
- ✅ **Startup Events** - Application initialization

## 🗄️ Database Schema

### Bus Collection
```json
{
  "_id": "ObjectId",
  "bus_number": "BUS001",
  "bus_name": "Express Travels",
  "bus_type": "ac",
  "source": "New York",
  "destination": "Boston",
  "departure_time": "ISODate",
  "arrival_time": "ISODate",
  "total_seats": 40,
  "available_seats": 35,
  "booked_seats": 5,
  "seats": [
    {
      "seat_number": "A1",
      "seat_type": "window",
      "price": 500.0,
      "status": "booked",
      "passenger_name": "John Doe",
      "passenger_email": "john@example.com"
    }
  ],
  "created_at": "ISODate"
}
```

## 🧪 Testing

### Manual Testing with Swagger UI
1. Visit http://localhost:8000/docs
2. Try all endpoints interactively
3. Test error scenarios

### Example Test Cases
```python
# test_buses.py (Basic example)
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_all_buses():
    response = client.get("/buses/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_bus():
    bus_data = {
        "bus_number": "TEST001",
        "bus_name": "Test Bus",
        "bus_type": "ac",
        "source": "TestSource",
        "destination": "TestDest",
        "departure_time": "2024-01-15T08:00:00",
        "arrival_time": "2024-01-15T12:00:00",
        "total_seats": 40
    }
    response = client.post("/buses/", json=bus_data)
    assert response.status_code == 201
```

## 🚀 Deployment

### Local Development
```bash
uvicorn main:app --reload --port 8000
```

### Production Deployment
```bash
# Install production server
pip install uvicorn[standard]

# Run with multiple workers
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Environment Variables for Production
```env
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/
DATABASE_NAME=bus_booking_prod
```

## 👨‍🏫 Teaching Guide

### Learning Path for Junior Developers

#### Week 1: FastAPI Fundamentals
1. **Day 1**: Basic FastAPI setup and first endpoints
2. **Day 2**: Path parameters and query parameters
3. **Day 3**: Request bodies with Pydantic models
4. **Day 4**: Response models and validation
5. **Day 5**: Error handling and status codes

#### Week 2: Database & Architecture
1. **Day 1**: MongoDB connection and basic operations
2. **Day 2**: CRUD operations implementation
3. **Day 3**: Service layer and business logic
4. **Day 4**: Dependency injection pattern
5. **Day 5**: Modular routers and project structure

#### Week 3: Advanced Features
1. **Day 1**: Search and filtering functionality
2. **Day 2**: Complex business logic (booking system)
3. **Day 3**: Data validation and constraints
4. **Day 4**: API documentation and testing
5. **Day 5**: Project completion and review

#### Week 4: Real-world Extensions
1. **Day 1**: User authentication and authorization
2. **Day 2**: Payment integration
3. **Day 3**: Email notifications
4. **Day 4**: Caching and performance
5. **Day 5**: Deployment and monitoring

### Key Learning Objectives
- Understand RESTful API design principles
- Master FastAPI's dependency injection system
- Learn proper error handling and validation
- Implement database operations with MongoDB
- Practice clean code architecture patterns
- Use automatic API documentation effectively

## 🛠️ Troubleshooting

### Common Issues

1. **MongoDB Connection Failed**
   - Check if MongoDB is running: `mongod`
   - Verify connection string in `.env` file

2. **Import Errors**
   - Ensure all `__init__.py` files are present
   - Check Python path and virtual environment

3. **Port Already in Use**
   ```bash
   # Find and kill process
   lsof -ti:8000 | xargs kill -9
   # Or use different port
   uvicorn main:app --reload --port 8001
   ```

4. **Module Not Found**
   ```bash
   # Install requirements
   pip install -r requirements.txt
   # Or install individually
   pip install fastapi uvicorn pymongo python-dotenv pydantic
   ```

## 🤝 Contributing

This project is perfect for learning FastAPI. To extend it:

1. Fork the repository
2. Create a feature branch
3. Add new functionality
4. Test thoroughly
5. Submit a pull request

### Suggested Extensions
- User authentication system
- Payment gateway integration
- Email ticket delivery
- Admin dashboard
- Real-time seat availability
- Booking history and management

## 📄 License

This project is created for educational purposes. Feel free to use and modify for learning FastAPI.

## 🆘 Support

For questions or issues:
1. Check the FastAPI documentation: https://fastapi.tiangolo.com/
2. Review PyMongo documentation: https://pymongo.readthedocs.io/
3. Examine the automatic API docs at `/docs`

---

**Happy Coding!** 🚀 Build amazing APIs with FastAPI!
