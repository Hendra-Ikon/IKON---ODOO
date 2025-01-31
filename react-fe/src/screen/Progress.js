import React, { useState, useEffect } from 'react';
import { FaRegCommentDots } from 'react-icons/fa';
import Select from 'react-select';
import { signOut } from 'firebase/auth'; // Firebase signOut
import { useNavigate } from 'react-router-dom'; // React Router for navigation
import { auth } from '../firebaseConfig'; // Import Firebase auth instance

function Progress() {
  const [tableData, setTableData] = useState([]);
  const [showOverlay, setShowOverlay] = useState(false);
  const [commentData, setCommentData] = useState(null);
  const navigate = useNavigate(); // React Router navigation

  useEffect(() => {
    // Fetch data from API
    const fetchTimesheets = async () => {
        try {
            const response = await fetch('http://localhost:8042/graphql/timesheet', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Basic ' + btoa('zaki123hanan@gmail.com:testing'),
                    'Cookie': 'session_id=b278ca885cb0c88b45364cab72649d40254eb010;',
                },
                body: JSON.stringify({
                    query: `
                        query {
                            timesheets {
                                projectName
                                activityName
                                duration
                                description
                                date
                                state
                                status
                            }
                        }
                    `,
                }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const result = await response.json();
            setTableData(result.data.timesheets);
        } catch (error) {
            console.error('Error fetching timesheets:', error);
        }
      };

      fetchTimesheets();
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('jwtToken'); // Remove JWT token from localStorage
  
    signOut(auth) // Use Firebase auth signOut
      .then(() => {
        console.log('User logged out successfully.');
        navigate('/'); // Navigate directly to the home page
        setTimeout(() => {
          window.location.reload(); // Refresh the page after redirect
        }, 100); // Add a slight delay to ensure navigation happens first
      })
      .catch((error) => {
        console.error('Error during logout:', error); // Log any errors
      });
  };

  const formatHoursToHM = (hours) => {
    const totalMinutes = Math.floor(hours * 60);
    const hrs = Math.floor(totalMinutes / 60);
    const mins = totalMinutes % 60;
    return `${hrs}h ${mins}m`;
  };

  const totalHours = tableData.reduce((total, item) => total + item.hoursSpent, 0);

  const handleCommentClick = (data) => {
    setCommentData(data);
    setShowOverlay(true);
  };

  const handleCloseOverlay = () => {
    setShowOverlay(false);
    setCommentData(null);
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="bg-white p-6 rounded-lg shadow-lg text-center w-full max-w-2xl">
        {/* Header with Logout */}
        <div className="flex justify-between items-center mb-4">
          <h1 className="text-2xl font-bold text-green-500">Progress Tracker</h1>
          <button
            onClick={handleLogout}
            className="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600"
          >
            Logout
          </button>
        </div>

        <h2 className="text-xl font-semibold text-gray-700">
          Attendance Submitted Successfully!
        </h2>
        <p className="mt-4 text-gray-700">Your attendance has been recorded.</p>
        <p className="mt-2 text-gray-500">{new Date().toLocaleDateString()}</p>

        {/* Table to display project data */}
        <div className="mt-6 overflow-x-auto">
          <table className="min-w-full bg-white border border-gray-300 text-left">
            <thead>
              <tr>
                <th className="px-4 py-2 border-b-2 font-semibold">Project Name</th>
                <th className="px-4 py-2 border-b-2 font-semibold">Activity Name</th>
                <th className="px-4 py-2 border-b-2 font-semibold">Hours Spent</th>
              </tr>
            </thead>
            <tbody>
              {tableData.map((item, index) => (
                <tr key={index} className="border-b">
                  <td className="px-4 py-2 border-r">{item.projectName}</td>
                  <td className="px-4 py-2 border-r">{item.activityName}</td>
                  <td className="px-4 py-2 flex items-center">
                    {formatHoursToHM(item.hoursSpent)}
                    <FaRegCommentDots
                      className="ml-2 text-blue-500 cursor-pointer"
                      onClick={() => handleCommentClick(item)}
                    />
                  </td>
                </tr>
              ))}
              {/* Total row */}
              <tr>
                <td colSpan="2" className="px-4 py-2 font-semibold text-right border-r">Total</td>
                <td className="px-4 py-2 font-semibold">{formatHoursToHM(totalHours)}</td>
              </tr>
            </tbody>
          </table>
        </div>

        {/* Add Progress button */}
        <div className="mt-6">
          <button
            onClick={() => setShowOverlay(true)}
            className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
          >
            Add Progress
          </button>
        </div>
      </div>

      {/* Overlay for comment details */}
      {showOverlay && commentData && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="relative bg-white rounded-lg shadow-lg w-full max-w-lg p-6">
            <button
              onClick={handleCloseOverlay}
              className="absolute top-2 right-2 bg-red-500 text-white rounded-full px-2"
            >
              ✕
            </button>
            <h2 className="text-xl font-bold mb-4">Progress Details</h2>
            <p><strong>Project Name:</strong> {commentData.projectName}</p>
            <p><strong>Activity Name:</strong> {commentData.activityName}</p>
            <p><strong>Date:</strong> {commentData.date}</p>
            <div className="mt-4">
              <label className="block text-gray-700 font-semibold mb-1">Description:</label>
              <textarea
                className="w-full px-4 py-2 border rounded-lg"
                value={commentData.description}
                readOnly
              />
            </div>
          </div>
        </div>
      )}

      {/* Overlay for Progress form */}
      {showOverlay && !commentData && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="relative bg-white rounded-lg shadow-lg w-full max-w-lg p-6">
            <button
              onClick={handleCloseOverlay}
              className="absolute top-2 right-2 bg-red-500 text-white rounded-full px-2"
            >
              ✕
            </button>
            <ProgressForm onClose={handleCloseOverlay} />
          </div>
        </div>
      )}
    </div>
  );
}

const ProgressForm = ({ onClose }) => {
  const [selectedProject, setSelectedProject] = useState('');
  const [tasks, setTasks] = useState([]);
  const [selectedTask, setSelectedTask] = useState('');
  const [description, setDescription] = useState('');
  const [date] = useState(new Date().toISOString().substring(0, 10));
  const [hours, setHours] = useState(0);
  const [minutes, setMinutes] = useState(0);

  const handleSave = () => {
    console.log('Save progress logic not implemented yet.');
    onClose();
  };

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4 text-center">New Progress</h1>
      <div className="mb-4">
        <label className="block text-gray-700 font-semibold mb-1">Project</label>
        <Select
          options={[
            { value: 'Project A', label: 'Project A' },
            { value: 'Project B', label: 'Project B' },
          ]}
          onChange={(option) => setSelectedProject(option.value)}
        />
      </div>
      <div className="mb-4">
        <label className="block text-gray-700 font-semibold mb-1">Task</label>
        <Select
          options={[
            { value: 'Task A1', label: 'Task A1' },
            { value: 'Task A2', label: 'Task A2' },
          ]}
          onChange={(option) => setSelectedTask(option.value)}
        />
      </div>
      <div className="mb-4">
        <label className="block text-gray-700 font-semibold mb-1">Description</label>
        <textarea
          className="w-full px-4 py-2 border rounded-lg"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
      </div>
      <div className="mb-4">
        <label className="block text-gray-700 font-semibold mb-1">Date</label>
        <input type="date" className="w-full px-4 py-2 border rounded-lg bg-gray-100" value={date} disabled />
      </div>
      <div className="flex justify-between">
        <button
          onClick={handleSave}
          className="bg-blue-500 text-white py-2 px-4 rounded-lg"
        >
          Save
        </button>
        <button onClick={onClose} className="text-gray-500 hover:underline">
          Cancel
        </button>
      </div>
    </div>
  );
};

export default Progress;
