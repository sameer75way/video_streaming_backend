from sqlmodel import SQLModel

# Import models so Alembic sees them
from app.models import User, Role

__all__ = ["SQLModel"]