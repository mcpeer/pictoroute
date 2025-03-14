from fastapi import APIRouter, File, UploadFile
from typing import List
from pictoroute.core.get_coordinates import append_coordinates_to_address
from pictoroute.core.image_processing import process_images
from pictoroute.core.route_planning import create_path
from pictoroute.models.address import Address
from pictoroute.models.shortest_path import ShortestPath

router = APIRouter()


@router.post("/process-images")
async def process_images_route(images: List[UploadFile] = File(...)) -> List[Address]:
    """
    Process a list of images and return a dict of addresses.
    
    Args:
        images (List[UploadFile]): A list of image files to be processed.
        
    Returns:
        dict: A dictionary of addresses extracted from the images.
    """
    # Process the uploaded images
    addresses = await process_images(images)

    # Get coordinates for the addresses
    addresses_with_coordinates = [append_coordinates_to_address(address) for address in addresses]
    
    # Addresses
    return addresses_with_coordinates


@router.post("/refetch-coordinates")
async def refetch_coordinates_route(addresses: List[Address]) -> List[Address]:
    """
    Refetch coordinates for a list of addresses.
    
    Args:
        addresses (List[dict]): A list of addresses to refetch coordinates for.
        
    Returns:
        dict: A dictionary of addresses with updated coordinates.
    """
    # Get coordinates for the addresses where coordinates is None, otherwise keep the existing coordinates
    addresses_with_coordinates = [append_coordinates_to_address(address) if address.coordinates is None or address.to_update else address for address in addresses]

    # Set to_update to False for all addresses
    for address in addresses_with_coordinates:
        address.to_update = False
    
    # Addresses
    return addresses_with_coordinates


@router.post("/get-shortest-path")
async def get_shortest_path_route(addresses: list[Address]) -> ShortestPath:
    """
    Get the shortest path through a list of addresses.
    
    Args:
        addresses (list[Address]): A list of addresses to find the shortest path through.
        
    Returns:
        list[Address]: A list of addresses in the shortest path order.
    """
    # Get the shortest path through the addresses
    path = create_path(addresses)
    
    # Return the addresses in the shortest path order
    return path