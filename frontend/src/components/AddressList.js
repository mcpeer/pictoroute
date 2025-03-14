import React, { useState } from 'react';
import { refetchCoordinates, getShortestPath } from '../api';
import ShortestPath from './ShortestPath';
import { FaEdit } from 'react-icons/fa'; // Importing an edit icon from react-icons
import { Cat } from 'lucide-react';

const AddressList = ({ addresses, setAddresses }) => {
  const [isFetching, setIsFetching] = useState(false);
  const [shortestPath, setShortestPath] = useState(null);

  const handleRefetchCoordinates = async (index) => {
    setIsFetching(true);
    // reset shortestPath
    setShortestPath(null);
    const updatedAddresses = await refetchCoordinates([addresses[index]]);
    const newAddresses = [...addresses];
    newAddresses[index] = updatedAddresses[0];

    // Reset to_update only if coordinates are present
    if (updatedAddresses[0].coordinates) {
      newAddresses[index].to_update = false; // Collapse the edit fields
    }

    setAddresses(newAddresses);
    setIsFetching(false);
  };

  const handlePlanRoute = async () => {
    const path = await getShortestPath(addresses);
    setShortestPath(path);  // Store the result for rendering
  };

  const handleInputChange = (index, field, value) => {
    const updatedAddresses = [...addresses];
    updatedAddresses[index] = { ...updatedAddresses[index], [field]: value };
    setAddresses(updatedAddresses);
  };

  const handleEditClick = (index) => {
    const updatedAddresses = [...addresses];
    updatedAddresses[index] = { ...updatedAddresses[index], to_update: true };
    setAddresses(updatedAddresses);
  };

  return (
    <div className="p-6 bg-white flex flex-col items-center">
      {/* Nyan Cat animation wrapper */}
      <div className="relative w-24 h-24 mb-4">
        {/* Rainbow trail animation */}
        <div className="absolute inset-0 animate-pulse">
          <div className="absolute left-0 w-full h-2 bg-red-500 transform -translate-x-1/2" style={{ top: '20%' }} />
          <div className="absolute left-0 w-full h-2 bg-yellow-500 transform -translate-x-1/3" style={{ top: '35%' }} />
          <div className="absolute left-0 w-full h-2 bg-green-500 transform -translate-x-1/4" style={{ top: '50%' }} />
          <div className="absolute left-0 w-full h-2 bg-blue-500 transform -translate-x-1/5" style={{ top: '65%' }} />
        </div>
        {/* Cat icon with animation */}
        <div className="absolute inset-0 flex items-center justify-center animate-bounce">
          <Cat size={48} className="text-gray-800" />
        </div>
      </div>

      <h2 className="text-xl font-bold mb-4">Extracted Addresses</h2>
      <ul className="w-full">
        {addresses.map((address, index) => (
          <li key={index} className="mb-4 border p-4 rounded-lg bg-gray-50 flex flex-col">
            <div className="flex justify-between">
              <div>
                {address.coordinates ? (
                  <>
                    <p>
                      <strong>{address.street_name}</strong>, {address.house_number}, {address.postal_code}, {address.city}
                    </p>
                    <p className="text-green-500">✔ Coordinates: {address.coordinates.latitude}, {address.coordinates.longitude}</p>
                  </>
                ) : (
                  <>
                    <p>
                      <strong>{address.street_name}</strong>, {address.house_number}, {address.postal_code}, {address.city}
                    </p> 
                    <p className="text-red-500">No coordinates found</p>
                  </>
                )}
              </div>
              {/* Edit Icon */}
              <button onClick={() => handleEditClick(index)} className="text-gray-500 hover:text-blue-500">
                <FaEdit />
              </button>
            </div>

            {address.to_update && (
              <div className="flex flex-col mb-2 mt-2">
                <input
                  type="text"
                  placeholder="Street Name"
                  value={address.street_name}
                  onChange={(e) => handleInputChange(index, 'street_name', e.target.value)}
                  className="p-2 border rounded mb-1"
                />
                <input
                  type="text"
                  placeholder="House Number"
                  value={address.house_number}
                  onChange={(e) => handleInputChange(index, 'house_number', e.target.value)}
                  className="p-2 border rounded mb-1"
                />
                <input
                  type="text"
                  placeholder="Postal Code"
                  value={address.postal_code}
                  onChange={(e) => handleInputChange(index, 'postal_code', e.target.value)}
                  className="p-2 border rounded mb-1"
                />
                <input
                  type="text"
                  placeholder="City"
                  value={address.city}
                  onChange={(e) => handleInputChange(index, 'city', e.target.value)}
                  className="p-2 border rounded mb-1"
                />
                <button
                  onClick={() => handleRefetchCoordinates(index)}
                  className="px-3 py-1 bg-yellow-500 text-white rounded-md hover:bg-yellow-600"
                >
                  {isFetching ? 'Fetching...' : 'Refetch Coordinates'}
                </button>
              </div>
            )}
          </li>
        ))}
      </ul>
      {addresses.every(addr => addr.coordinates) && !shortestPath && (
        <button
          onClick={handlePlanRoute}
          className="mt-4 px-6 py-2 bg-green-500 text-white rounded-md hover:bg-green-600"
        >
          Plan Route
        </button>
      )}

      {shortestPath && <ShortestPath path={shortestPath} />}
    </div>
  );
};

export default AddressList;
