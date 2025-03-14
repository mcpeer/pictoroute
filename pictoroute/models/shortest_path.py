from pydantic import BaseModel
from typing import Optional

from pictoroute.models.address import Address

class ShortestPath(BaseModel):
    length: float  # Length of the path in km
    gmaps_links: list[str]  # List of Google Maps links for each chunk
    addresses: list[Address]  # List of addresses in the path
