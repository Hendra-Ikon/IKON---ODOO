import React, { useState, useEffect, useRef } from 'react';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import * as XLSX from 'xlsx';
import { useNavigate } from 'react-router-dom';

const API_URL = 'https://ikon-attendance-api.azurewebsites.net/api/attendance/report';

const Administrator = () => {
  const [startDate, setStartDate] = useState(null);
  const [jwtToken, setJwtToken] = useState('');
  const [reportData, setReportData] = useState([]);
  const [statusFilter, setStatusFilter] = useState(''); // State for status filter
  const tableContainerRef = useRef(null);
  const scrollbarRef = useRef(null);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('jwtToken');
    if (token) {
      setJwtToken(token);
    } else {
      navigate('/');
      window.location.reload();
    }
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem('jwtToken');
    localStorage.removeItem('loginType');
    navigate('/');
    window.location.reload();
  };

  const fetchReport = async (downloadExcel = false) => {
    if (!startDate) {
      alert("Please select a date before generating the report.");
      return;
    }

    const submittedFrom = new Date(startDate).toISOString();
    const submittedTo = new Date(new Date(startDate).setDate(new Date(startDate).getDate() + 1) - 1000).toISOString();

    const reportPayload = {
      SubmittedFrom: submittedFrom,
      SubmittedTo: submittedTo
    };

    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${jwtToken}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(reportPayload)
      });

      if (response.ok) {
        const result = await response.json();
        if (downloadExcel) {
          downloadExcelFile(result);
        } else {
          setReportData(result);
        }
      } else {
        console.error('Error fetching report:', await response.text());
      }
    } catch (error) {
      console.error('Error fetching report:', error);
    }
  };

  const downloadExcelFile = (data) => {
    const formattedData = data.map(({ employee, attendance }) => ({
      Email: employee?.email || 'N/A',
      Name: employee?.name || 'N/A',
      Status: attendance ? getStatusText(attendance.status) : 'N/A',
      Location: attendance?.location || 'N/A',
      Latitude: attendance?.latitude || 'N/A',
      Longitude: attendance?.longitude || 'N/A',
      HealthCondition: attendance ? getHealthConditionText(attendance.healthcondition) : 'N/A',
      Note: attendance?.note || 'N/A',
      TimeSubmitted: attendance ? new Date(attendance.submittedat).toLocaleString() : 'N/A'
    }));

    const worksheet = XLSX.utils.json_to_sheet(formattedData);
    const workbook = XLSX.utils.book_new();
    const localDate = startDate.toLocaleDateString('en-CA'); // Formats the date as 'YYYY-MM-DD'
    XLSX.utils.book_append_sheet(workbook, worksheet, 'Attendance Report');
    XLSX.writeFile(workbook, `Attendance_Report_${localDate}.xlsx`);
  };

  const getStatusText = (status) => {
    switch (status) {
      case 1: return 'WFO';
      case 2: return 'WFH';
      case 3: return 'Sick Leave';
      case 4: return 'Annual Leave';
      case 5: return 'Half Day Leave';
      default: return 'Unknown';
    }
  };

  const getHealthConditionText = (condition) => {
    switch (condition) {
      case 1: return 'Healthy';
      case 2: return 'Some family members unwell';
      case 3: return 'Feeling unwell';
      case 4: return 'Both self and family unwell';
      default: return 'Unknown';
    }
  };

  const syncScroll = () => {
    if (tableContainerRef.current && scrollbarRef.current) {
      scrollbarRef.current.scrollLeft = tableContainerRef.current.scrollLeft;
    }
  };

  // Filter report data by selected status
  const filteredReportData = statusFilter
    ? reportData.filter(({ attendance }) => getStatusText(attendance?.status) === statusFilter)
    : reportData;

  return (
    <div className="min-h-screen flex flex-col items-center bg-gray-100 p-4">
      <div className="w-full max-w-full bg-white shadow-md rounded-lg p-6">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-bold text-blue-600">Ikon Support App</h1>
          <button
            className="bg-teal-500 text-white px-4 py-2 rounded-md hover:bg-teal-600"
            onClick={handleLogout}
          >
            LOGOUT
          </button>
        </div>

        <div className="mb-4">
          <h3 className="text-blue-600 text-lg font-semibold">Attendance Report</h3>
          <div className="flex space-x-2 items-center mt-2">
            <DatePicker
              selected={startDate}
              onChange={(date) => setStartDate(date)}
              className="border border-gray-300 rounded-md p-2 w-full max-w-xs"
              placeholderText="mm/dd/yyyy"
            />
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="border border-gray-300 rounded-md p-2 w-full max-w-xs"
            >
              <option value="">All Status</option>
              <option value="WFO">WFO</option>
              <option value="WFH">WFH</option>
              <option value="Sick Leave">Sick Leave</option>
              <option value="Annual Leave">Annual Leave</option>
              <option value="Half Day Leave">Half Day Leave</option>
            </select>
            <button
              className="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600"
              onClick={() => fetchReport(false)}
            >
              GENERATE PREVIEW
            </button>
            <button
              className="bg-green-500 text-white px-4 py-2 rounded-md hover:bg-green-600"
              onClick={() => fetchReport(true)}
            >
              DOWNLOAD EXCEL
            </button>
          </div>
        </div>

        {filteredReportData.length > 0 && (
          <div
            ref={tableContainerRef}
            onScroll={syncScroll}
            className="overflow-x-auto overflow-y-auto pb-16"
            style={{ maxHeight: '70vh' }}
          >
            <table className="min-w-full bg-white border">
              <thead>
                <tr>
                  <th className="px-4 py-2 border">Email</th>
                  <th className="px-4 py-2 border">Name</th>
                  <th className="px-4 py-2 border">Status</th>
                  <th className="px-4 py-2 border">Location</th>
                  <th className="px-4 py-2 border">Latitude</th>
                  <th className="px-4 py-2 border">Longitude</th>
                  <th className="px-4 py-2 border">Map</th>
                  <th className="px-4 py-2 border">Health Condition</th>
                  <th className="px-4 py-2 border">Note</th>
                  <th className="px-4 py-2 border">Time Submitted</th>
                </tr>
              </thead>
              <tbody>
                {filteredReportData.map(({ employee, attendance }, index) => (
                  <tr key={index} className="text-sm">
                    <td className="px-4 py-2 border whitespace-nowrap">{employee?.email || 'N/A'}</td>
                    <td className="px-4 py-2 border whitespace-nowrap">{employee?.name || 'N/A'}</td>
                    <td className="px-4 py-2 border whitespace-nowrap">{attendance ? getStatusText(attendance.status) : 'N/A'}</td>
                    <td className="px-4 py-2 border whitespace-nowrap">{attendance?.location || 'N/A'}</td>
                    <td className="px-4 py-2 border whitespace-nowrap">{attendance?.latitude || 'N/A'}</td>
                    <td className="px-4 py-2 border whitespace-nowrap">{attendance?.longitude || 'N/A'}</td>
                    <td className="px-4 py-2 border whitespace-nowrap">
                      {attendance?.latitude && attendance?.longitude ? (
                        <a
                          href={`https://www.google.com/maps/search/?api=1&query=${attendance.latitude},${attendance.longitude}`}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-blue-500 hover:underline"
                        >
                          View on Map
                        </a>
                      ) : (
                        'N/A'
                      )}
                    </td>
                    <td className="px-4 py-2 border whitespace-nowrap">{attendance ? getHealthConditionText(attendance.healthcondition) : 'N/A'}</td>
                    <td className="px-4 py-2 border whitespace-nowrap">{attendance?.note || 'N/A'}</td>
                    <td className="px-4 py-2 border whitespace-nowrap">{attendance ? new Date(attendance.submittedat).toLocaleString() : 'N/A'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
      <div
        ref={scrollbarRef}
        className="fixed bottom-0 left-0 right-0 bg-white border-t overflow-x-auto"
        onScroll={(e) => tableContainerRef.current.scrollLeft = e.target.scrollLeft}
      >
        <div style={{ width: tableContainerRef.current ? tableContainerRef.current.scrollWidth : '100%' }}></div>
      </div>
    </div>
  );
};

export default Administrator;
