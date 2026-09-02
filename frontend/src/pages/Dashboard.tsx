import React, { useState, useEffect } from 'react';
import api from '../api';

interface Device {
  id: number;
  hostname: string;
  ip_address: string;
  status: string;
}

export default function Dashboard() {
  const [devices, setDevices] = useState<Device[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchDevices = async () => {
    setLoading(true);
    try {
      // Create a dummy token for local SQLite bypass if auth isn't fully set up yet
      const res = await api.get('/devices/');
      setDevices(res.data);
    } catch (error) {
      console.error("Failed to fetch devices:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDevices();
  }, []);

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-800">Network Dashboard</h2>
        <button 
          onClick={fetchDevices} 
          className="bg-blue-600 text-white px-4 py-2 rounded shadow hover:bg-blue-700 transition"
        >
          Refresh Devices
        </button>
      </div>
      
      {loading ? (
        <p className="text-gray-500">Loading devices...</p>
      ) : (
        <div className="bg-white shadow rounded-lg overflow-hidden">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-100">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Hostname</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">IP Address</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {devices.length === 0 ? (
                <tr>
                  <td colSpan={4} className="px-6 py-4 text-center text-gray-500">No devices found.</td>
                </tr>
              ) : (
                devices.map(device => (
                  <tr key={device.id}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{device.id}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{device.hostname}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{device.ip_address}</td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={px-2 inline-flex text-xs leading-5 font-semibold rounded-full }>
                        {device.status}
                      </span>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
