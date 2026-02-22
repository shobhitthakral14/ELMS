"""
Entry point to run the FastAPI application
"""
import uvicorn
from app.config import HOST, PORT

if __name__ == "__main__":
    print("\n" + "="*70)
    print("HR LEAVE MANAGEMENT SYSTEM - BACKEND")
    print("="*70)
    print("\nStarting server...")
    print(f"API Documentation: http://localhost:{PORT}/docs")
    print(f"Alternative Docs:  http://localhost:{PORT}/redoc")
    print(f"Health Check:      http://localhost:{PORT}/health")
    print("\n" + "="*70 + "\n")

    # For now, use the legacy main file until routers are fully implemented
    uvicorn.run("app.legacy_main:app", host=HOST, port=PORT, reload=True, log_level="info")
