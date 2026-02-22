"""
Configuration settings for the application
"""
import os

# Security Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production-min-32-chars")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24 hours

# Database Configuration
DATABASE_URL = "sqlite:///./leave_management.db"

# CORS Configuration
CORS_ORIGINS = ["*"]  # In production, replace with specific origins

# Server Configuration
HOST = "0.0.0.0"
PORT = 8001
