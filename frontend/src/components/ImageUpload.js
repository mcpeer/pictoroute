import React, { useState } from 'react';
import { processImages } from '../api';
import { Cat } from 'lucide-react';

const ImageUpload = ({ setAddresses }) => {
  const [images, setImages] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleImageChange = (e) => {
    setImages([...e.target.files]);
  };

  const handleExtractAddresses = async () => {
    setLoading(true);
    const result = await processImages(images);
    setAddresses(result);
    setLoading(false);
  };

  return (
    <div className="p-6 bg-gray-100 min-h-[400px] flex flex-col items-center justify-center space-y-6">
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

      <h1 className="text-3xl font-bold text-gray-800 text-center mb-8">
        Pictoroute
      </h1>
      <div className="w-full max-w-md">
        <p className="text-gray-800 text-center mb-1"><i>Crop your images to the address area only</i></p>
        <p className="text-gray-800 text-center mb-1"><i>Ensure images are clear and well-lit</i></p>
      </div>

      {/* File input wrapper */}
      <div className="w-full max-w-md">
        <label className="flex flex-col items-center px-4 py-6 bg-white rounded-lg shadow-lg cursor-pointer hover:bg-gray-50 transition-colors">
          <span className="mb-2 text-sm font-medium text-gray-600">
            Select images to extract addresses
          </span>
          <input
            type="file"
            multiple
            onChange={handleImageChange}
            className="hidden"
          />
          <span className="text-blue-500 hover:text-blue-600">
            Browse files
          </span>
          {images.length > 0 && (
            <span className="mt-2 text-sm text-gray-500">
              {images.length} {images.length === 1 ? 'file' : 'files'} selected
            </span>
          )}
        </label>
      </div>

      {/* Extract button */}
      <button
        onClick={handleExtractAddresses}
        disabled={loading || images.length === 0}
        className={`
          mt-6 px-8 py-3 rounded-full
          font-medium text-white
          transform transition-all duration-200
          ${loading || images.length === 0 
            ? 'bg-gray-400 cursor-not-allowed' 
            : 'bg-gradient-to-r from-blue-500 to-purple-600 hover:scale-105 hover:shadow-lg'
          }
        `}
      >
        {loading ? (
          <span className="flex items-center space-x-2">
            <svg
              className="animate-spin h-5 w-5"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle 
                className="opacity-25" 
                cx="12" 
                cy="12" 
                r="10" 
                stroke="currentColor" 
                strokeWidth="4" 
              />
              <path 
                className="opacity-75" 
                fill="currentColor" 
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" 
              />
            </svg>
            <span>Processing...</span>
          </span>
        ) : (
          'Extract Addresses'
        )}
      </button>
    </div>
  );
};

export default ImageUpload;