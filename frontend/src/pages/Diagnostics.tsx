import React, { useState } from 'react';
import api from '../api';

export default function Diagnostics() {
  const [host, setHost] = useState('');
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const runPing = async () => {
    if (!host) return;
    setLoading(true);
    setResult(null);
    try {
      const res = await api.post('/diagnostics/ping', { host });
      setResult(res.data);
    } catch (err: any) {
      setResult({ error: err.response?.data?.detail || err.message });
    }
    setLoading(false);
  };

  const runSubnet = async () => {
    if (!host) return;
    setLoading(true);
    setResult(null);
    try {
      const res = await api.post('/diagnostics/subnet', { cidr: host });
      setResult(res.data);
    } catch (err: any) {
      setResult({ error: err.response?.data?.detail || err.message });
    }
    setLoading(false);
  };

  return (
    <div className="max-w-2xl mx-auto">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">Network Diagnostics</h2>
      
      <div className="bg-white p-6 rounded-lg shadow-md mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">Target Host / IP / CIDR</label>
        <input 
          type="text" 
          value={host}
          onChange={(e) => setHost(e.target.value)}
          placeholder="e.g. 8.8.8.8 or 192.168.1.0/24"
          className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 mb-4"
        />
        
        <div className="flex space-x-4">
          <button 
            onClick={runPing}
            disabled={loading || !host}
            className="flex-1 bg-green-600 text-white py-2 px-4 rounded-md shadow hover:bg-green-700 disabled:opacity-50 transition"
          >
            {loading ? 'Running...' : 'Run Ping Test'}
          </button>
          
          <button 
            onClick={runSubnet}
            disabled={loading || !host}
            className="flex-1 bg-indigo-600 text-white py-2 px-4 rounded-md shadow hover:bg-indigo-700 disabled:opacity-50 transition"
          >
            {loading ? 'Calculating...' : 'Subnet Calculator'}
          </button>
        </div>
      </div>

      {result && (
        <div className="bg-gray-900 rounded-lg shadow-md overflow-hidden">
          <div className="px-4 py-2 bg-gray-800 text-gray-200 text-sm font-semibold border-b border-gray-700">
            Output Results
          </div>
          <pre className="p-4 text-green-400 text-sm overflow-x-auto whitespace-pre-wrap">
            {JSON.stringify(result, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}
