import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Diagnostics from './pages/Diagnostics';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50 text-gray-900 flex flex-col">
        <nav className="bg-blue-600 text-white p-4 shadow-md">
          <div className="container mx-auto flex justify-between items-center">
            <h1 className="text-xl font-bold tracking-wider">NetGuardian</h1>
            <div className="space-x-6">
              <Link to="/" className="hover:text-blue-200 transition-colors">Dashboard</Link>
              <Link to="/diagnostics" className="hover:text-blue-200 transition-colors">Diagnostics</Link>
            </div>
          </div>
        </nav>
        
        <main className="flex-1 container mx-auto p-6">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/diagnostics" element={<Diagnostics />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
