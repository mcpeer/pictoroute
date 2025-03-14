import React, { useState } from 'react';
import ImageUpload from './components/ImageUpload';
import AddressList from './components/AddressList';

function App() {
  const [addresses, setAddresses] = useState(null);

  return (
    <div className="min-h-screen bg-gray-200 flex items-center justify-center">
      {!addresses ? (
        <ImageUpload setAddresses={setAddresses} />
      ) : (
        <AddressList addresses={addresses} setAddresses={setAddresses} />
      )}
    </div>
  );
}

export default App;
