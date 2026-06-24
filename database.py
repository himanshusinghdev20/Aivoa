from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from config import settings

engine = None
SessionLocal = None

try:
    engine = create_engine(
        settings.DATABASE_URL,
        echo=settings.DEBUG,
        pool_pre_ping=True
    )

    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )

except Exception as e:
    print(f"Database initialization error: {e}")

Base = declarative_base()


def get_db():
    if SessionLocal is None:
        return

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    try:
        if engine:
            Base.metadata.create_all(bind=engine)
            print("Database connected")
    except Exception as e:
        print(f"Database connection failed: {e}")
        print("Continuing without database")