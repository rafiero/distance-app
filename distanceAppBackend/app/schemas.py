from pydantic import BaseModel


class DistanceQueryBase(BaseModel):
    source_address: str
    destination_address: str


class DistanceQueryCreate(DistanceQueryBase):
    pass


class DistanceQueryRead(DistanceQueryBase):
    id: int
    distance_km: float

    class Config:
        from_attributes = True
