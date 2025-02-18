from sqlalchemy import Column, Integer, String, Float
from app.database import Base


class DistanceQuery(Base):
    __tablename__ = "distance_queries"

    id = Column(Integer, primary_key=True, index=True)
    source_address = Column(String, nullable=False)
    destination_address = Column(String, nullable=False)
    distance_km = Column(Float, nullable=False)
