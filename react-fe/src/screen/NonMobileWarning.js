import React from 'react';

function NonMobileWarning() {
  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="bg-white p-6 rounded-lg shadow-lg text-center max-w-lg">
        <h1 className="text-2xl font-bold text-red-500">Mobile Access Only</h1>
        <p className="mt-4 text-gray-700">
          This website is only accessible on mobile devices and tablets.
        </p>
        <p className="mt-2 text-gray-600">
          Please access this site using a mobile device or tablet to continue.
        </p>
      </div>
    </div>
  );
}

export default NonMobileWarning;