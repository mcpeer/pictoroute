import json
from geopy.geocoders import Nominatim

from pictoroute.models.address import Address, Coordinates


def load_addresses_from_file_with_json_string(file_path: str) -> dict:
    """Load addresses from file with json string."""
    # load addresses in the following format 
    # {{
    #  "addresses": [
    #  {{
    #  "street": "string",
    #  "house_number": "string",
    #  "postalcode": "string",
    #  "city": "string"
    #  }},
    #  ...
    #  ]
    # }}
    with open(file_path, "r") as f:
        addresses = json.loads(f.read())

    return addresses


def geocode_with_fallback(geolocator, address: Address):
    attempts = [
        f"{address.street_name} {address.house_number} {address.postal_code[:6]} {address.city}",
        f"{address.street_name} {address.house_number} {address.city}",
    ]
    
    for attempt in attempts:
        location = geolocator.geocode(attempt, exactly_one=True)
        if location:
            return location
    
    return None


def append_coordinates_to_address(address: Address) -> Address:
    """Get coordinates for address."""
    geolocator = Nominatim(user_agent="test_app", timeout=5)
    
    location = geocode_with_fallback(geolocator, address)

    if location:
        coordinates = Coordinates(
            latitude=location.latitude,
            longitude=location.longitude,
        )
        address.coordinates = coordinates
    return address


if __name__ == "__main__":
    addresses = load_addresses_from_file_with_json_string('tests/test_addresses.txt')
    addresses_with_coordinates = []

    # add coordinates to addresses 
    for address in addresses:
        address = Address(**address)
        address = append_coordinates_to_address(address)
        addresses_with_coordinates.append(address)
        
    # save to file
    with open('tmp_with_coordinates.txt', 'w') as f:
        f.write(json.dumps([address.dict() for address in addresses_with_coordinates], indent=2))

