# main.py
from fastapi import FastAPI
from config.database import database
from routers import buses

# Initialize FastAPI app 
app = FastAPI(
    title="Bus Ticket Booking API",
    description="A complete bus ticket booking system with seat management",
    version="1.0.0"
)

# Connect to database on startup
@app.on_event("startup")
async def startup_event():
    print("🚀 Starting Bus Booking API...")
    if database.connect():
        print("✅ Database connection established during startup")
    else:
        print("⚠️  Starting without database connection")

# Include routers
app.include_router(buses.router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to Bus Ticket Booking API",
        "docs": "Visit /docs for Swagger UI",
        "version": "1.0.0",
        "database_status": "connected" if database.is_connected else "disconnected"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "database": "connected" if database.is_connected else "disconnected"
    }