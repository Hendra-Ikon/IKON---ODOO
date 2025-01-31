import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [envUsername, setEnvUsername] = useState('');
  const [envPassword, setEnvPassword] = useState('');
  const [envEmail, setEnvEmail] = useState('');
  const navigate = useNavigate();
  const clientId = '184138638066-9bqo1pfduq1g9bnuai567lfjch3sfp72.apps.googleusercontent.com';

  useEffect(() => {
    setEnvUsername(process.env.REACT_APP_USERNAME);
    setEnvPassword(process.env.REACT_APP_PASSWORD);
    setEnvEmail(process.env.REACT_APP_EMAIL);

    const script = document.createElement('script');
    script.src = 'https://accounts.google.com/gsi/client';
    script.async = true;
    script.onload = () => {
      window.google.accounts.id.initialize({
        client_id: clientId,
        callback: onSignIn,
      });
      window.google.accounts.id.renderButton(
        document.getElementById('signInDiv'),
        { theme: 'outline', size: 'large' }
      );
    };
    document.body.appendChild(script);

    return () => {
      document.body.removeChild(script);
    };
  }, [clientId]);

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

  const onSignIn = async (response) => {
    const idToken = response.credential;

    if (idToken) {
      const decoded = decodeJwt(idToken);
      const { name: Name, email: Email } = decoded;

      await authenticateUser(Name, Email, 'google');
    } else {
      alert('Google Sign-In failed. Please try again.');
    }
  };

  const authenticateUser = async (Name, Email, loginType) => {
    try {
      const res = await fetch('https://ikon-attendance-api.azurewebsites.net/api/token', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ Name, Email }),
      });

      if (!res.ok) {
        throw new Error(`API error: ${res.status} - ${res.statusText}`);
      }

      const data = await res.json();
      const { token } = data;

      if (!token) {
        throw new Error('No JWT token received');
      }

      // Store the token and login type
      localStorage.setItem('jwtToken', token);
      localStorage.setItem('loginType', loginType);

      // Redirect based on login type
      if (loginType === 'google') {
        navigate('/attendance', { replace: true });
        window.location.reload(); // Refresh the page after Google login
      } else if (loginType === 'traditional') {
        navigate('/administrator', { replace: true });
        window.location.reload();
      }
    } catch (error) {
      console.error('JWT token retrieval error:', error);
      alert('An error occurred while retrieving the JWT token. Please try again.');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Check if the input matches the environment credentials
    if (username === envUsername && password === envPassword) {
      await authenticateUser(envUsername, envEmail, 'traditional');
    } else {
      alert('Invalid username or password. Please try again.');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="w-full max-w-md bg-white p-8 rounded-lg shadow-md">
        <h1 className="text-2xl font-bold text-center mb-6">Login</h1>

        <div className="mb-4 p-4 bg-blue-100 rounded-lg text-blue-800">
          <p className="flex items-center">
            <span className="mr-2">✅</span>
            For employees, please log in with your Google Account
          </p>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-gray-700">Username</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Enter username"
              className="w-full px-4 py-2 mt-2 border rounded-lg"
            />
          </div>

          <div className="mb-6">
            <label className="block text-gray-700">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter password"
              className="w-full px-4 py-2 mt-2 border rounded-lg"
            />
          </div>

          <button
            type="submit"
            className="w-full bg-blue-500 text-white font-bold py-2 px-4 rounded-lg hover:bg-blue-600"
          >
            LOGIN
          </button>
        </form>

        <div className="text-center my-4 text-gray-500">or</div>

        <div id="signInDiv" className="d-grid"></div>
      </div>
    </div>
  );
}

export default LoginPage;
