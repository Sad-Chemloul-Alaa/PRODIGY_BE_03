from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=settings.CONNECT_ARGS, # used for SQLITE specefication
    pool_size=5,       # Number of persistent connections
    max_overflow=10,   # Extra connections allowed temporarily
    pool_timeout=30,   # Wait time if no connection is available
    pool_recycle=1800  # Reconnect after 30 min
)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()
