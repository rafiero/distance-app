import pytest
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.database import Base
from app import crud, schemas

TEST_DATABASE_URL = "sqlite:///:memory:"  # For demonstration


@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    """
    Creates and configures a database session for testing.

    - Uses an in-memory SQLite database (TEST_DATABASE_URL).
    - Creates all tables defined via SQLAlchemy.
    - Yields a test session and closes it after the test finishes.
    """
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_create_distance_query(db_session) -> None:
    """
    Tests the creation of a distance query in the database.

    Steps:
    1. Prepare source and destination addresses via DistanceQueryCreate.
    2. Invoke `create_distance_query` to store and calculate the distance.
    3. Verify that the result is not None and the calculated distance is greater than zero.
    """
    query_data = schemas.DistanceQueryCreate(
        source_address="Rio Branco, Acre, Brazil",
        destination_address="Avenida Paulista, 1578, Bela Vista, São Paulo, SP, Brazil"
    )
    db_result = crud.create_distance_query(db_session, query_data)
    assert db_result is not None
    assert db_result.distance_km > 0
