import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { auth } from '../firebaseConfig';
import { onAuthStateChanged, signOut } from 'firebase/auth';

// NonMobileWarning modal component
const NonMobileWarning = () => (
  <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
    <div className="bg-white p-6 rounded-lg shadow-lg text-center max-w-sm mx-auto">
      <h2 className="text-xl font-semibold text-red-600 mb-4">Warning</h2>
      <p className="text-gray-700 mb-4">
        This site is optimized for mobile and tablet devices. Please access it on a mobile or tablet.
      </p>
    </div>
  </div>
);

// Enhanced mobile detection hook with additional platform checks
const useMobileCheck = () => {
  const [isMobile, setIsMobile] = useState(false);

  const checkMobile = () => {
    const userAgent = navigator.userAgent || navigator.vendor || window.opera;

    // Basic mobile checks based on user agent
    const isMobileDevice = /Android|iPhone|iPod|webOS|BlackBerry|IEMobile|Opera Mini/i.test(userAgent);
    const isTabletDevice = /iPad|Tablet|PlayBook|Silk/i.test(userAgent);
    const isIPadOS = navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1;

    // Additional checks to detect mobile devices more reliably
    const isTouchScreen = window.matchMedia('(pointer: coarse)').matches;
    const isMobileScreen = window.innerWidth <= 768 || window.innerHeight <= 1024;

    // Platform check to ensure we are on mobile OS, not just emulated mobile dimensions on a desktop browser
    const isMobilePlatform = /Android|iPhone|iPad|iPod|webOS/i.test(navigator.platform);

    // Check to exclude desktop versions of major browsers
    const isDesktopChrome = /Chrome/.test(userAgent) && !/Mobile/.test(userAgent);
    const isDesktopFirefox = /Firefox/.test(userAgent) && !/Mobile/.test(userAgent);
    const isDesktopSafari = /Safari/.test(userAgent) && !/Mobile/.test(userAgent) && !/iPad|iPhone/.test(userAgent);
    const isDesktopEdge = /Edg/.test(userAgent) && !/Mobile/.test(userAgent);
    const isDesktopOpera = /OPR/.test(userAgent) && !/Mobile/.test(userAgent);

    // Final mobile check with all conditions combined
    const mobileCheckResult = (
      (isMobileDevice || isTabletDevice || isIPadOS) &&
      isTouchScreen &&
      isMobileScreen &&
      isMobilePlatform && // Ensures that we're on an actual mobile platform
      !(isDesktopChrome || isDesktopFirefox || isDesktopSafari || isDesktopEdge || isDesktopOpera) // Excludes desktop browsers
    );

    setIsMobile(mobileCheckResult);

    if (!mobileCheckResult) {
      console.log("Non-mobile device detected. Showing warning modal.");
    }
  };

  useEffect(() => {
    if (process.env.REACT_APP_ENABLE_MOBILE_ONLY === 'true') {
      // Initial mobile check
      checkMobile();

      // Add listeners to dynamically check on window resize or orientation change
      window.addEventListener('resize', checkMobile);
      window.addEventListener('orientationchange', checkMobile);

      // Add a slight delay to re-check for emulation inconsistencies on initial load
      const initialCheckTimeout = setTimeout(checkMobile, 100);

      // Set an interval to periodically check in case of emulation
      const intervalId = setInterval(checkMobile, 5000);

      return () => {
        clearTimeout(initialCheckTimeout);
        clearInterval(intervalId);
        window.removeEventListener('resize', checkMobile);
        window.removeEventListener('orientationchange', checkMobile);
      };
    } else {
      setIsMobile(true); // Allow all devices if mobile-only restriction is disabled
    }
  }, []);

  return isMobile;
};

function AttendanceForm() {
  const isMobile = useMobileCheck();
  const navigate = useNavigate();
  const [user, setUser] = useState({ name: '', email: '' });
  const [location, setLocation] = useState('');
  const [coordinates, setCoordinates] = useState([0, 0]);
  const [accuracy, setAccuracy] = useState(0);
  const [status, setStatus] = useState('');
  const [healthCondition, setHealthCondition] = useState('');
  const [note, setNote] = useState('');
  const [error, setError] = useState('');
  const [geolocationError, setGeolocationError] = useState('');
  const [showNote, setShowNote] = useState(false);
  const [showLocationPopup, setShowLocationPopup] = useState(true);
  const [loading, setLoading] = useState(true);
  const [locationFetched, setLocationFetched] = useState(false); // Flag to track if reverse geocode is done
  const [submitting, setSubmitting] = useState(false); // New state for handling multiple clicks
  const [gpsSpoofed, setGpsSpoofed] = useState(false); // New state for GPS spoofing detection
  const [locationPermissionDenied, setLocationPermissionDenied] = useState(false); // New state for permission
  const [previousAccuracy, setPreviousAccuracy] = useState(null);
  const [mapSrc, setMapSrc] = useState("");

  const decodeJwt = (token) => {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split('')
        .map((c) => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
        .join('')
    );
    return JSON.parse(jsonPayload);
  };

  useEffect(() => {
    const token = localStorage.getItem('jwtToken');
    if (!token) {
      console.log('No token found, redirecting to login...');
      navigate('/');
    } else {
      const decoded = decodeJwt(token);
      setUser({
        name: decoded.name || '',
        email: decoded.email || '',
      });
    }
  }, [navigate]);

  useEffect(() => {
    onAuthStateChanged(auth, (currentUser) => {
      if (currentUser) {
        setUser({
          name: currentUser.displayName,
          email: currentUser.email,
        });
      } else {
        setUser((prev) => prev);
      }
    });
  }, []);

  useEffect(() => {
    const token = localStorage.getItem('jwtToken');
    if (!token) {
      console.log('No token found, redirecting to login...');
      navigate('/');
    } else {
      const decoded = decodeJwt(token);
      console.log('Decoded JWT Token:', decoded); // Log the decoded token
      setUser({
        name: decoded.name || '',
        email: decoded.email || '',
      });
    }
  }, [navigate]);  

  useEffect(() => {
    const checkUserSubmission = async () => {
      try {
        console.log('Initiating API call to check user submission...');
  
        const token = localStorage.getItem('jwtToken');
        if (!token) {
          console.log('No token found, redirecting to login...');
          navigate('/');
          return;
        }
  
        const decoded = decodeJwt(token);
        console.log('Decoded JWT Token:', decoded); // Debug log to inspect decoded token
  
        if (!decoded.email) {
          console.error('Decoded token does not contain an email field. Aborting check.');
          setError('Invalid user token. Please log in again.');
          navigate('/');
          return;
        }
  
        const response = await fetch('https://ikon-attendance-api.azurewebsites.net/api/attendance/report', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          },
          body: JSON.stringify({
            SubmittedFrom: new Date().toISOString().split('T')[0] + 'T00:00:00Z',
            SubmittedTo: new Date().toISOString().split('T')[0] + 'T23:59:59Z',
          }),
        });
  
        console.log('API response status:', response.status);
  
        if (!response.ok) {
          throw new Error('Failed to fetch attendance data.');
        }
  
        const data = await response.json();
        console.log('Parsed API response data:', data); // Debug log for API response
  
        // Match email and check submittedat field
        const currentUserEmail = decoded.email.toLowerCase();
        console.log('Current user email:', currentUserEmail); // Debug log for current user email
  
        const userEntries = data.filter(
          (entry) =>
            entry.employee?.email?.toLowerCase() === currentUserEmail && // Match email from `employee.email`
            entry.attendance?.submittedat && // Ensure submittedat exists
            entry.attendance.submittedat.trim() !== '' // Ensure submittedat is not blank or whitespace
        );
  
        console.log('Filtered results for the current user with valid submittedat:', userEntries);
  
        // Redirect only if a valid submission exists
        if (userEntries.length > 0) {
          console.log('User has submitted attendance today. Redirecting to progress.');
          navigate('/progress');
        } else {
          console.log('No valid submissions found for the current user.');
          setLoading(false); // Allow the user to fill the form
        }
      } catch (err) {
        console.error('Error occurred during API call:', err);
        setError('An error occurred while checking attendance. Please try again.');
      }
    };
  
    if (user.email) {
      checkUserSubmission();
    }
  }, [user, navigate]);
  
  const handleLogout = () => {
    localStorage.removeItem('jwtToken');

    signOut(auth)
      .then(() => {
        console.log('User logged out successfully.');
        window.location.reload();
        setTimeout(() => {
          navigate('/');
        }, 100);
      })
      .catch((error) => {
        console.error('Error during logout:', error);
      });
  };

  useEffect(() => {
    const fetchLocation = () => {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const lat = position.coords.latitude;
          const lon = position.coords.longitude;
          const accuracy = position.coords.accuracy;
  
          setCoordinates([lat.toFixed(8), lon.toFixed(8)]);
          setAccuracy(accuracy);
  
          // Enhanced fake GPS detection logic
          if (process.env.REACT_APP_ENABLE_GPS_SPOOFING === 'true') {
            const isSuspiciousAccuracy = accuracy < 1 || accuracy > 50;
            const isIntegerAccuracy = accuracy % 1 === 0;
            const isLargeAccuracyJump = previousAccuracy && Math.abs(previousAccuracy - accuracy) > 20;

            if (isSuspiciousAccuracy || isIntegerAccuracy || isLargeAccuracyJump) {
              setGpsSpoofed(true);
              console.log("GPS spoofing detected based on enhanced criteria.");
              setGeolocationError('GPS data may not be reliable due to potential spoofing.');
              setLoading(false);
              setLocationPermissionDenied(false);
              return;
            }
          }
  
          setCoordinates([lat.toFixed(8), lon.toFixed(8)]);
          setPreviousAccuracy(accuracy); // Update previous accuracy for next check
          setLoading(false);
          setGpsSpoofed(false);
          setLocationPermissionDenied(false);
        },
        (error) => {
          setLoading(false);
          if (error.code === error.PERMISSION_DENIED) {
            setLocationPermissionDenied(true);
          } else {
            setGeolocationError('Unable to retrieve location. Please check your device settings.');
          }
        },
        {
          enableHighAccuracy: true,
          maximumAge: 0,
          timeout: 10000,
        }
      );
    };
  
    fetchLocation();
    const intervalId = setInterval(fetchLocation, 10000);
  
    return () => clearInterval(intervalId);
  }, [previousAccuracy]);   

  useEffect(() => {
    if (coordinates[0] !== 0 && coordinates[1] !== 0 && !locationFetched) {
      reverseGeocode(coordinates[0], coordinates[1]);
      setLocationFetched(true); // Set the flag to avoid re-running
    }
  }, [coordinates, locationFetched]);

  const reverseGeocode = async (lat, lon) => {
    try {
      const response = await fetch(
        `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lon}&zoom=10`
      );

      if (!response.ok) {
        throw new Error(`Geocoding error: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();
      const city = data.address.city || data.address.county || 'Unknown Location';
      const postalCode = data.address.postcode ? `, ${data.address.postcode}` : '';

      setLocation(`${city}${postalCode}`);
    } catch (error) {
      console.error('Reverse geocoding failed:', error);
      setGeolocationError('Unable to fetch location data.');
    }
  };

  useEffect(() => {
    if (coordinates[0] !== 0 && coordinates[1] !== 0) {
      setMapSrc(
        `https://www.openstreetmap.org/export/embed.html?bbox=${
          parseFloat(coordinates[1]) - 0.0025
        },${parseFloat(coordinates[0]) - 0.0025},${parseFloat(coordinates[1]) + 0.0025},${
          parseFloat(coordinates[0]) + 0.0025
        }&layer=mapnik&marker=${coordinates[0]},${coordinates[1]}&zoom=19`
      );
    }
  }, [coordinates]);

  const handleHealthConditionChange = (e) => {
    const value = e.target.value;
    setHealthCondition(value);
    setShowNote(
      value === 'I am healthy but some of my family members are feeling unwell' ||
      value === 'I am feeling unwell but my family members are healthy' ||
      value === 'My family members and I are feeling unwell'
    );
  };

  const mapStatusToInteger = (status) => {
    switch (status) {
      case 'WFO':
        return 1;
      case 'WFH':
        return 2;
      case 'Sick Leave':
        return 3;
      case 'Annual Leave':
        return 4;
      case 'Half Day Leave':
        return 5;
      default:
        return 0;
    }
  };

  const mapHealthConditionToInteger = (condition) => {
    switch (condition) {
      case 'My family members and I are healthy':
        return 1;
      case 'I am healthy but some of my family members are feeling unwell':
        return 2;
      case 'I am feeling unwell but my family members are healthy':
        return 3;
      case 'My family members and I are feeling unwell':
        return 4;
      default:
        return 0;
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (submitting) return; // Prevent multiple clicks

    setSubmitting(true);

    const timeSubmitted = new Date().toISOString();
    const statusInt = mapStatusToInteger(status);
    const healthConditionInt = mapHealthConditionToInteger(healthCondition);

    const formData = {
      id: 0,
      email: user.email,
      name: user.name,
      location,
      submittedat: timeSubmitted,
      status: statusInt,
      note: note || null,
      latitude: coordinates[0],
      longitude: coordinates[1],
      healthcondition: healthConditionInt,
    };

    if (!formData.email || !formData.name || !status || !location || !healthCondition || (showNote && !note)) {
      setError('Please fill in all required fields.');
      setSubmitting(false);
      return;
    }

    console.log("Submitting form data:", formData);

    try {
      const token = localStorage.getItem('jwtToken');

      const response = await fetch('https://ikon-attendance-api.azurewebsites.net/api/attendance', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        console.log('Data saved successfully!');
        navigate('/success');
      } else {
        const errorMsg = await response.text();
        console.error('Error saving data:', errorMsg);

        if (errorMsg.includes("Your latest submission has been rejected")) {
          setError('You have already submitted your attendance for today.');
        } else {
          setError('Failed to save data. Please try again.');
        }
      }
    } catch (error) {
      console.error('Error during submission:', error);
      setError('An error occurred during submission.');
    } finally {
      setSubmitting(false);
    }
  };

  if (!isMobile) {
    return <NonMobileWarning />;
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      {locationPermissionDenied && (
        <div className="fixed top-0 left-0 right-0 bottom-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
          <div className="bg-white p-6 rounded-lg shadow-lg text-center">
            <p className="text-lg text-gray-800">Please enable location services to continue.</p>
            <p className="text-sm text-gray-600 mt-2">We need access to your location to proceed. Refresh this page to continue</p>
          </div>
        </div>
      )}

      {gpsSpoofed && (
        <div className="fixed top-0 left-0 right-0 bottom-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
          <div className="bg-white p-6 rounded-lg shadow-lg text-center">
            <p className="text-lg font-bold text-red-600">GPS Spoofing Detected</p>
            <p className="text-gray-800 mt-2">GPS data may not be reliable. Please disable any spoofing apps and refresh this page to proceed.</p>
            {/* Remove the close button to prevent bypassing */}
          </div>
        </div>
      )}

      {loading && !locationPermissionDenied && !gpsSpoofed && (
        <div className="text-center">Loading your location...</div>
      )}
  
      <div className="w-full max-w-lg bg-white p-8 rounded-lg shadow-md">
        <h1 className="text-2xl font-bold text-center text-blue-600 mb-4">Attendance Form</h1>

        <p className="text-center text-gray-600 mb-8">
          {new Date().toLocaleDateString('en-GB', {
            weekday: 'long',
            day: 'numeric',
            month: 'long',
            year: 'numeric',
          })}
        </p>
  
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4">
            <strong className="font-bold">Error: </strong>
            <span className="block sm:inline">{error}</span>
          </div>
        )}
  
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-gray-700">Email</label>
            <input
              type="email"
              value={user.email || ''}
              disabled
              className="w-full px-4 py-2 mt-2 border rounded-lg bg-gray-100"
            />
          </div>
  
          <div className="mb-4">
            <label className="block text-gray-700">Name</label>
            <input
              type="text"
              value={user.name || ''}
              disabled
              className="w-full px-4 py-2 mt-2 border rounded-lg bg-gray-100"
            />
          </div>
  
          <div className="mb-4">
            <label className="block text-gray-700">Status <span className="text-red-500">*</span></label>
            <select
              value={status}
              onChange={(e) => setStatus(e.target.value)}
              required
              className="w-full px-4 py-2 mt-2 border rounded-lg"
            >
              <option value="" disabled>Select a Status...</option>
              <option value="WFO">WFO</option>
              <option value="WFH">WFH</option>
              <option value="Sick Leave">Sick Leave</option>
              <option value="Annual Leave">Annual Leave</option>
              <option value="Half Day Leave">Half Day Leave</option>
            </select>
          </div>
  
          <div className="mb-4">
            <label className="block text-gray-700">Location <span className="text-red-500">*</span></label>
            <input
              type="text"
              value={location}
              onChange={(e) => setLocation(e.target.value)}
              required
              className="w-full px-4 py-2 mt-2 border rounded-lg"
              placeholder="Enter or modify location..."
            />
          </div>
  
          <div className="mb-4">
            <label className="block text-gray-700">Health Condition <span className="text-red-500">*</span></label>
            <select
              value={healthCondition}
              onChange={handleHealthConditionChange}
              required
              className="w-full px-4 py-2 mt-2 border rounded-lg"
            >
              <option value="" disabled>Select a Health Condition...</option>
              <option value="My family members and I are healthy">My family members and I are healthy</option>
              <option value="I am healthy but some of my family members are feeling unwell">I am healthy but some of my family members are feeling unwell</option>
              <option value="I am feeling unwell but my family members are healthy">I am feeling unwell but my family members are healthy</option>
              <option value="My family members and I are feeling unwell">My family members and I are feeling unwell</option>
            </select>
          </div>
  
          {showNote && (
            <div className="mb-4">
              <label className="block text-gray-700">Note <span className="text-red-500">*</span></label>
              <textarea
                rows="3"
                value={note}
                onChange={(e) => setNote(e.target.value)}
                required // Make the note field required if it's showing
                className="w-full px-4 py-2 mt-2 border rounded-lg"
                placeholder="Enter your note here..."
              />
            </div>
          )}

           {/* Map with dynamic src */}
          <div className="mb-4">
            <h3 className="block text-gray-700 mb-3">Current Location (may be inaccurate)</h3>
            <div style={{ overflow: 'hidden', width: '100%', height: '300px', borderRadius: '8px' }}>
              <iframe
                src={mapSrc}
                width="100%"
                height="300"
                allowFullScreen=""
                loading="lazy"
                style={{ border: 0, pointerEvents: 'none' }}
              ></iframe>
            </div>
            <p className="text-sm text-blue-600 underline text-center mt-2">
              <a
                href={`https://www.openstreetmap.org/?mlat=${coordinates[0]}&mlon=${coordinates[1]}&zoom=19`}
                target="_blank"
                rel="noopener noreferrer"
              >
                View larger map
              </a>
            </p>
          </div>
  
          <button
            type="submit"
            className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700"
            disabled={submitting || gpsSpoofed} // Disable the button if submitting
          >
            {submitting ? 'Submitting...' : 'Submit'}
          </button>
        </form>
  
        <button
          onClick={handleLogout}
          className="w-full bg-red-600 text-white py-2 mt-4 rounded-lg hover:bg-red-700"
        >
          Logout
        </button>
      </div>
    </div>
  );
}

export default AttendanceForm;