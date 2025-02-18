import math
from typing import Optional, Tuple, List, Type

import requests
from sqlalchemy.orm import Session
from app import models, schemas
from app.models import DistanceQuery

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"


def get_coordinates(address: str) -> Optional[Tuple[float, float]]:
    """
    Retrieves latitude and longitude for a given address using the Nominatim API.

    :param address: The address to geocode (street, city, country, etc.).
    :return: A tuple (latitude, longitude) if found, or None if the address could not be geocoded.
    """
    params = {
        "q": address,
        "format": "json",
        "limit": 1
    }
    # https://github.com/maksimKorzh/one-time-scrapers/blob/master/scrapers/reverse_geocoding/reverse_geocoding.py
    headers = {
        'User-Agent': 'MyDistanceApp/1.0'
    }
    response = requests.get(NOMINATIM_URL, params=params, headers=headers)
    data = response.json()
    if not data:
        return None
    return float(data[0]["lat"]), float(data[0]["lon"])


def calculate_distance_km(lat1, lon1, lat2, lon2) -> float:
    """
    Calculates the distance in kilometers between two geographic coordinates
    using the Haversine formula.

    :param lat1: Latitude of the first coordinate in decimal degrees.
    :param lon1: Longitude of the first coordinate in decimal degrees.
    :param lat2: Latitude of the second coordinate in decimal degrees.
    :param lon2: Longitude of the second coordinate in decimal degrees.
    :return: Distance in kilometers.
    """
    # https://www.geeksforgeeks.org/haversine-formula-to-find-distance-between-two-points-on-a-sphere/
    # https://www.youtube.com/watch?v=4S1ydVk01DQ
    # Earth radius in km
    R = 6371
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = (math.sin(d_lat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(d_lon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def create_distance_query(db: Session, query_data: schemas.DistanceQueryCreate) -> Optional[models.DistanceQuery]:
    """
    Creates a new DistanceQuery record in the database, calculating the distance
    between the source and destination addresses.

    :param db: A SQLAlchemy database session.
    :param query_data: An object containing source_address and destination_address.
    :return: The newly created DistanceQuery object, or None if coordinates could not be fetched.
    """
    coords_source = get_coordinates(query_data.source_address)
    coords_dest = get_coordinates(query_data.destination_address)
    if not coords_source or not coords_dest:
        return None  # Indicate failure

    lat1, lon1 = coords_source
    lat2, lon2 = coords_dest
    distance_km = calculate_distance_km(lat1, lon1, lat2, lon2)

    db_query = models.DistanceQuery(
        source_address=query_data.source_address,
        destination_address=query_data.destination_address,
        distance_km=distance_km,
    )
    db.add(db_query)
    db.commit()
    db.refresh(db_query)
    return db_query


def get_all_queries(db: Session) -> list[Type[DistanceQuery]]:
    """
    Retrieves all DistanceQuery records from the database.

    :param db: A SQLAlchemy database session.
    :return: A list of all DistanceQuery objects stored in the database.
    """
    return db.query(models.DistanceQuery).all()
