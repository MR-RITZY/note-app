from fastapi import APIRouter, Depends, Request
from fastapi.routing import APIRoute
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db

router = APIRouter(tags=["Roots"])

@router.get("/")
def root(request: Request, db: Session = Depends(get_db)):
    
    try:
        db.execute(text("SELECT 1"))
        db_status = "Connected"
    except Exception as e:
        db_status = f"Error: {str(e)}"

    
    routes_info = []
    for route in request.app.routes: 
        if isinstance(route, APIRoute):
            routes_info.append({
                "path": route.path,
                "methods": list(route.methods),
                "name": route.name
            })

    return {
        "name": "Note App API",
        "message": "Welcome to the Note API! 🚀",
        "docs": "/docs",
        "redoc": "/redoc",
        "version": "1.0.0",
        "database_status": db_status,
        "routes": routes_info,
        "status": "Note API is up and running"
    }
