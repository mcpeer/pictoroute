import React, { useState } from 'react';
import { MapContainer, TileLayer, Polyline, Marker, Popup } from 'react-leaflet';
import L from 'leaflet';

// Utility to create marker icon
const createMarkerIcon = (index) => {
  return L.divIcon({
    className: 'custom-icon',
    html: `<div class="flex items-center justify-center w-6 h-6 bg-blue-500 text-white rounded-full">${index + 1}</div>`,
  });
};

const ShortestPath = ({ path }) => {
  const [copyStatus, setCopyStatus] = useState('');
  
  const positions = path.addresses
    .filter(address => address.coordinates)
    .map(address => [address.coordinates.latitude, address.coordinates.longitude]);

  // Function to copy text using different methods
  const copyToClipboard = async (text) => {
    try {
      // Try using the Clipboard API first
      if (navigator.clipboard && window.isSecureContext) {
        await navigator.clipboard.writeText(text);
        return true;
      }
      
      // Fallback: Create temporary textarea element
      const textArea = document.createElement('textarea');
      textArea.value = text;
      
      // Make the textarea hidden but present in the DOM
      textArea.style.position = 'fixed';
      textArea.style.left = '-999999px';
      textArea.style.top = '-999999px';
      document.body.appendChild(textArea);
      
      // Select and copy the text
      textArea.focus();
      textArea.select();
      
      try {
        document.execCommand('copy');
        textArea.remove();
        return true;
      } catch (err) {
        textArea.remove();
        return false;
      }
    } catch (err) {
      return false;
    }
  };

  // Handler for the copy button
  const handleCopyToClipboard = async () => {
    const addressList = path.addresses.map((address, index) =>
      `${index + 1}. ${address.street_name}, ${address.house_number}, ${address.postal_code}, ${address.city}`
    ).join('\n');
    
    const linksList = path.gmaps_links.map((link, index) =>
      `Route part ${index + 1}: ${link}`
    ).join('\n');
    
    const textToCopy = `Ordered Route Addresses:\n${addressList}\n\nGoogle Maps Links:\n${linksList}`;
    
    try {
      const success = await copyToClipboard(textToCopy);
      if (success) {
        setCopyStatus('Copied successfully!');
        setTimeout(() => setCopyStatus(''), 2000); // Clear status after 2 seconds
      } else {
        setCopyStatus('Failed to copy');
      }
    } catch (err) {
      setCopyStatus('Failed to copy');
      console.error('Copy failed:', err);
    }
  };

  return (
    <div className="p-6 bg-white rounded-lg">
      <h2 className="text-xl font-bold mb-4">Planned Route</h2>
      
      {/* Map rendering */}
      <div className="h-64 w-full mb-6">
        <MapContainer
          center={positions[0]}
          zoom={13}
          scrollWheelZoom={false}
          style={{ height: '100%', width: '100%' }}
        >
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          />
          {positions.map((position, index) => (
            <Marker
              key={index}
              position={position}
              icon={createMarkerIcon(index)}
            >
              <Popup>{path.addresses[index].street_name}</Popup>
            </Marker>
          ))}
          <Polyline positions={positions} color="blue" />
        </MapContainer>
      </div>

      {/* Ordered list of addresses */}
      <div className="mb-6">
        <h3 className="text-lg font-bold mb-2">Ordered Route Addresses</h3>
        <ol className="list-decimal list-inside">
          {path.addresses.map((address, index) => (
            <li key={index} className="mb-2">
              {address.street_name}, {address.house_number}, {address.postal_code}, {address.city}
            </li>
          ))}
        </ol>
      </div>

      {/* Google Maps links */}
      <div>
        <h3 className="text-lg font-bold mb-2">Google Maps Links</h3>
        {path.gmaps_links.map((link, index) => (
          <a
            key={index}
            href={link}
            target="_blank"
            rel="noopener noreferrer"
            className="block mb-2 text-blue-500 hover:underline"
          >
            Route part {index + 1}
          </a>
        ))}
      </div>

      {/* Copy Button and Status */}
      <div className="mt-4 flex items-center gap-4">
        <button
          onClick={handleCopyToClipboard}
          className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600"
        >
          Copy Route Info
        </button>
        {copyStatus && (
          <span className={`text-sm ${copyStatus.includes('Failed') ? 'text-red-500' : 'text-green-500'}`}>
            {copyStatus}
          </span>
        )}
      </div>
    </div>
  );
};

export default ShortestPath;