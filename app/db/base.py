from sqlmodel import SQLModel

# need these for alembic
from app.models import User, Role

__all__ = ["SQLModel"]