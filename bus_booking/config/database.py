# config/database.py
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.client = None
        self.db = None
        self.is_connected = False
        
    def connect(self):
        """Connect to MongoDB"""
        try:
            self.client = MongoClient(os.getenv("MONGODB_URL", "mongodb://localhost:27017/"))
            # Test the connection
            self.client.admin.command('ping')
            self.db = self.client[os.getenv("DATABASE_NAME", "bus_booking_system")]
            self.is_connected = True
            print("✅ MongoDB connected successfully!")
            return True
        except Exception as e:
            print(f"❌ MongoDB connection failed: {e}")
            self.is_connected = False
            return False
    
    def get_collection(self, collection_name):
        """Get a specific collection from database"""
        if self.is_connected and self.db is not None:
            return self.db[collection_name]
        else:
            print(f"❌ Database not connected. Cannot get collection '{collection_name}'")
            return None

# Create a global database instance
database = Database()