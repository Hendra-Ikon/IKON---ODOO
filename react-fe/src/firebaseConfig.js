// firebaseConfig.js
import { initializeApp } from 'firebase/app';
import { getAuth, GoogleAuthProvider, signInWithPopup, signOut } from 'firebase/auth';
import { getAnalytics } from 'firebase/analytics';

// Firebase configuration
const firebaseConfig = {
  apiKey: process.env.REACT_APP_FIREBASE_API_KEY,
  authDomain: process.env.REACT_APP_FIREBASE_AUTH_DOMAIN,
  projectId: process.env.REACT_APP_FIREBASE_PROJECT_ID,
  storageBucket: process.env.REACT_APP_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: process.env.REACT_APP_FIREBASE_MESSAGING_SENDER_ID,
  appId: process.env.REACT_APP_FIREBASE_APP_ID,
  measurementId: process.env.REACT_APP_FIREBASE_MEASUREMENT_ID
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const auth = getAuth(app);
const provider = new GoogleAuthProvider();

// Set the client ID explicitly if needed
const clientId = '184138638066-9bqo1pfduq1g9bnuai567lfjch3sfp72.apps.googleusercontent.com';
provider.setCustomParameters({
  client_id: clientId,
});

// Utility function to set a cookie
const setCookie = (name, value, days) => {
  const d = new Date();
  d.setTime(d.getTime() + days * 24 * 60 * 60 * 1000);
  document.cookie = `${name}=${value}; expires=${d.toUTCString()}; path=/`;
};

// Utility function to retrieve a cookie by name
const getCookie = (name) => {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
};

// Google sign-in function with explicit client ID and JWT retrieval
const signInWithGoogle = () => {
  console.log('Initializing Google sign-in...');
  return signInWithPopup(auth, provider)
    .then(async (result) => {
      const user = result.user;
      const name = user.displayName;
      const email = user.email;

      // Set cookies
      setCookie('userName', name, 7);
      setCookie('userEmail', email, 7);

      try {
        // Attempt to retrieve the JWT token
        const response = await fetch('https://ikon-attendance-api.azurewebsites.net/api/token', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ Name: name, Email: email })
        });
        const data = await response.json();
        
        if (!response.ok) {
          console.error(`API error: ${response.status} - ${response.statusText}`, data);
          throw new Error('Failed to retrieve JWT token from API');
        }

        const { token } = data;
        if (!token) {
          console.error('Token missing in response:', data);
          throw new Error('No JWT token received');
        }

        localStorage.setItem('jwtToken', token);
        console.log('JWT saved successfully');

      } catch (error) {
        console.error('JWT token retrieval error:', error);
        alert('An error occurred while retrieving the JWT token. Please try again.');
      }
    })
    .catch(error => {
      console.error('Google sign-in error:', error);
      alert('An error occurred during Google Sign-In. Please try again.');
    });
};

// Logout function to clear user data and cookies
const logout = () => {
  return signOut(auth)
    .then(() => {
      setCookie('userName', '', -1);
      setCookie('userEmail', '', -1);
      localStorage.removeItem('jwtToken');
      console.log('User signed out, cookies cleared, JWT removed');
    })
    .catch(error => {
      console.error('Error during sign-out:', error);
    });
};

// Retrieve JWT token from localStorage
const getJwtToken = () => localStorage.getItem('jwtToken');

export { auth, signInWithGoogle, logout, getCookie, getJwtToken };
