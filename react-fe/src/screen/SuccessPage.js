import React from 'react';
import { Link } from 'react-router-dom';

function SuccessPage() {
  return (
    <div className="flex items-center justify-center h-screen bg-gray-100">
      <div className="bg-white p-6 rounded-lg shadow-lg text-center">
        <h1 className="text-2xl font-bold text-green-500">Attendance Submitted Successfully!</h1>
        <p className="mt-4 text-gray-700">Your attendance has been recorded.</p>
        
        <div className="mt-6">
          <Link to="/" className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600">
            Go back to form
          </Link>
        </div>
      </div>
    </div>
  );
}

export default SuccessPage;
