from pydantic import BaseModel
from typing import Optional

class Coordinates(BaseModel):
    latitude: float   # Latitude as a float
    longitude: float  # Longitude as a float

class Address(BaseModel):
    street_name: str          # Street name as a string
    house_number: str         # House number as a string (e.g. "12a")
    postal_code: str          # Postal code as a string in NL format (e.g. "1234AB")
    city: str                 # city name as a string
    coordinates: Optional[Coordinates] = None  # Coordinates are optional
    to_update: bool = False  # Flag to indicate if the address needs to be updated