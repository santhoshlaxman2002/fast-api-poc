from sqlalchemy.orm import sessionmaker
from app.db.database import engine

SessionLocal = sessionmaker(
    bind=engine,
    # TODO: Need to add comment for the below two
    autoflush=False,
    autocommit=False
)

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()