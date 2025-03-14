 
from math import radians, sin, cos, sqrt, atan2
from xml.dom import minidom
from urllib.parse import quote_plus
from pictoroute.core.get_coordinates import load_addresses_from_file_with_json_string
from pictoroute.models.address import Address, Coordinates
from pictoroute.models.shortest_path import ShortestPath

START_ADDRESS = Address(
    street_name="Eemplein",
    house_number="65",
    postal_code="3812EA",
    city="Amersfoort",
    coordinates=Coordinates(latitude=52.1588444, longitude=5.3820278),
)

END_ADDRESS = Address(
    street_name="Eemplein",
    house_number="65",
    postal_code="3812EA",
    city="Amersfoort",
    coordinates=Coordinates(latitude=52.1588444, longitude=5.3820278),
)

# Function to calculate Haversine distance between two points
def haversine(coord1, coord2):
    R = 6371.0  # Radius of the Earth in kilometers
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    
    return distance

def nearest_neighbor_with_end(coordinates, start_index=0, end_index=None):
    n = len(coordinates)
    
    if end_index is None:
        end_index = n - 1  # Default: the last point if not provided
    
    # Ensure the start and end points are different
    if start_index == end_index:
        raise ValueError("Start and end points cannot be the same.")
    
    unvisited = set(range(n))
    path = [start_index]  # Start at the given starting point
    unvisited.remove(start_index)
    
    # If the end point is specified, we don't visit it until last
    if end_index in unvisited:
        unvisited.remove(end_index)

    while unvisited:
        last_visited = path[-1]
        # Find the nearest unvisited point
        next_point = min(unvisited, key=lambda i: haversine(coordinates[last_visited], coordinates[i]))
        path.append(next_point)
        unvisited.remove(next_point)

    # Now append the end point to the path
    path.append(end_index)

    return path

# Function to compute the total distance of a path
def total_distance(path, coordinates):
    dist = 0
    for i in range(len(path) - 1):
        dist += haversine(coordinates[path[i]], coordinates[path[i + 1]])
    # Return to the start
    dist += haversine(coordinates[path[-1]], coordinates[path[0]])
    return dist

def create_gmaps_links(path: list[int], addresses: list[Address], n_addresses_per_chunk: int = 10):
    # create chunks of n_addresses_per_chunk addresses
    # where the chunks are overlapping by 1 address
    chunks = [path[i:i + n_addresses_per_chunk] for i in range(0, len(path), n_addresses_per_chunk - 1)]
    
    # Generate a link for each chunk
    # make sure addresses are UrlEncoded
    # addresses can still contain special characters that need to be encoded
    # we can use urllib.parse.quote_plus for this
    url_encoded_addresses = [quote_plus(f"{address.street_name} {address.house_number} {address.postal_code[:6]} {address.city}") for address in addresses]
    gmaps_links = []
    for _, chunk in enumerate(chunks):
        # only process chunks with more than 1 address
        if len(chunk) <= 1:
            continue
        origin = url_encoded_addresses[chunk[0]]
        destination = url_encoded_addresses[chunk[-1]]
        waypoints = '|'.join([url_encoded_addresses[i] for i in chunk[1:-1]])
        gmaps_links.append(f"https://www.google.com/maps/dir/?api=1&origin={origin}&destination={destination}&travelmode=bicycle&waypoints={waypoints}")
    return gmaps_links

# Function to perform a 2-opt swap
def two_opt_swap(route, i, k):
    """Perform a 2-opt swap by reversing the order of nodes between i and k."""
    new_route = route[:i] + route[i:k + 1][::-1] + route[k + 1:]
    return new_route

# 2-opt optimization function with fixed start and end points
def two_opt_fixed_endpoints(coordinates, path):
    """Apply 2-opt algorithm to the given path with fixed start and end."""
    best_path = path
    best_distance = total_distance(best_path, coordinates)
    improved = True
    
    # Loop until no improvements can be made
    while improved:
        improved = False
        # Loop over all pairs (i, k) where i starts from the second node (to preserve start)
        # and k does not include the last node (to preserve end)
        for i in range(1, len(path) - 2):  # Avoid swapping the start point
            for k in range(i + 1, len(path) - 1):  # Avoid swapping the end point
                new_path = two_opt_swap(best_path, i, k)
                new_distance = total_distance(new_path, coordinates)
                if new_distance < best_distance:
                    best_path = new_path
                    best_distance = new_distance
                    improved = True
    
    return best_path

def create_path(addresses: list[Address], start_index=0, end_index=None) -> ShortestPath:
    # Add the start and end addresses to the list of addresses
    addresses = [START_ADDRESS] + addresses + [END_ADDRESS]

    # Get the coordinates from the addresses
    coordinates = [(address.coordinates.latitude, address.coordinates.longitude) for address in addresses]
    
    # Get the nearest neighbor path with the fixed start and end points
    path = nearest_neighbor_with_end(coordinates, start_index, end_index)

    # Apply 2-opt optimization to the path
    path = two_opt_fixed_endpoints(coordinates, path)
    
    # Calculate the total distance of the found path
    min_distance = total_distance(path, coordinates)

    # Create Gmaps links for each chunk of 10 addresses
    gmaps_links = create_gmaps_links(path, addresses)
    
    # Return the result
    return ShortestPath(length=min_distance, addresses=[addresses[i] for i in path], gmaps_links=gmaps_links)    

