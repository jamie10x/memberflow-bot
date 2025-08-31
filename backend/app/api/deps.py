# backend/app/api/deps.py
from ..core.database import SessionLocal

def get_db():
    """
    Dependency to get a database session.
    Ensures the session is closed after the request is finished.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()