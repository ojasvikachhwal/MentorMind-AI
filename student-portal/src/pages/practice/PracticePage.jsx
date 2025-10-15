import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { 
  Home as HomeIcon, 
  BookText, 
  FileText, 
  Cpu, 
  User
} from 'lucide-react';
import { getCurrentUser, logout } from '../../services/api';

const PracticePage = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const user = getCurrentUser();
  const [showUserMenu, setShowUserMenu] = useState(false);
  
  // Mock data for coding questions
  const codingQuestions = [
    'Coding question 1',
    'Coding question 2',
    'Coding question 3',
    'Coding question 4',
    'Coding question 5',
    'Coding question 6',
    'Coding question 7',
    'Coding question 8',
    'Coding question 9',
    'Coding question 10',
  ];

  const handleLogout = () => {
    logout();
    navigate('/login');
  };
  
  const toggleUserMenu = () => {
    setShowUserMenu(!showUserMenu);
  };

  const handleNavigation = (path) => {
    if (path === 'home') {
      navigate('/dashboard');
    } else {
      navigate(`/${path}`);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex">
      {/* Updated sidebar with exact dimensions */}
      <div 
        className="min-h-screen flex flex-col"
        style={{
          width: '260px',
          backgroundColor: '#202123',
          padding: '8px 0'
        }}
      >
        {/* Hamburger menu icon with exact 40x40 icon button */}
        <div style={{ 
          width: '40px', 
          height: '40px', 
          display: 'flex', 
          alignItems: 'center', 
          justifyContent: 'center', 
          margin: '4px auto', 
          borderRadius: '6px', 
          cursor: 'pointer',
          transition: 'background 0.2s ease'
        }}>
          <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </div>

        {/* Navigation buttons - with exact 40x40 icon buttons */}
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '8px' }}>
          {/* HOME icon with exact 40x40 touch target */}
          <div 
            style={{
              width: '40px',
              height: '40px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              borderRadius: '6px',
              cursor: 'pointer',
              transition: 'background 0.2s ease',
              backgroundColor: location.pathname === '/dashboard' ? '#f97316' : 'transparent',
              margin: '4px auto'
            }}
            onClick={() => handleNavigation('dashboard')}
          >
            <HomeIcon className="w-5 h-5 text-white" />
          </div>

          {/* PRACTICE icon with exact 40x40 touch target */}
          <div 
            style={{
              width: '40px',
              height: '40px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              borderRadius: '6px',
              cursor: 'pointer',
              transition: 'background 0.2s ease',
              backgroundColor: location.pathname === '/practice' ? '#f97316' : 'transparent',
              margin: '4px auto'
            }}
            onClick={() => handleNavigation('practice')}
          >
            <BookText className="w-5 h-5 text-white" />
          </div>

          {/* RESOURCE icon with exact 40x40 touch target */}
          <div 
            style={{
              width: '40px',
              height: '40px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              borderRadius: '6px',
              cursor: 'pointer',
              transition: 'background 0.2s ease',
              backgroundColor: location.pathname === '/resources' ? '#f97316' : 'transparent',
              margin: '4px auto'
            }}
            onClick={() => handleNavigation('resources')}
          >
            <FileText className="w-5 h-5 text-white" />
          </div>

          {/* VED icon with exact 40x40 touch target */}
          <div 
            style={{
              width: '40px',
              height: '40px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              borderRadius: '6px',
              cursor: 'pointer',
              transition: 'background 0.2s ease',
              backgroundColor: location.pathname === '/ved' ? '#f97316' : 'transparent',
              margin: '4px auto'
            }}
            onClick={() => handleNavigation('ved')}
          >
            <div className="flex items-center justify-center">
              <div className="w-5 h-5 text-white font-bold" style={{ fontWeight: 'bold', fontSize: '12px' }}>V</div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content Area - PRACTICE CONTENT */}
      <div className="flex-1 min-h-screen bg-white flex">
        {/* Top bar with user profile */}
        <div className="absolute top-0 right-0 p-4 z-10">
          <div className="relative">
            <button onClick={toggleUserMenu} className="bg-gray-800 rounded-full w-10 h-10 flex items-center justify-center">
              <User className="h-6 w-6 text-white" />
            </button>
            {showUserMenu && (
              <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg py-2 z-10">
                <a href="#" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded">Profile</a>
                <a href="#" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded">Contact Us</a>
                <a href="#" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded">Settings</a>
                <a href="#" onClick={handleLogout} className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded">Log Out</a>
              </div>
            )}
          </div>
        </div>

        {/* LEFT SIDEBAR - Coding questions list */}
        <div className="w-1/5 bg-gray-100 p-4 border-r border-gray-300">
          <h2 className="font-semibold mb-2">Coding Questions</h2>
          <div className="space-y-2">
            {codingQuestions.map((question, index) => (
              <div key={index} className="hover:bg-gray-200 p-2 rounded cursor-pointer">
                {question}
              </div>
            ))}
          </div>
        </div>

        {/* MAIN CENTER AREA - Code Editor */}
        <div className="flex-1 bg-white p-6">
          {/* Language selector and buttons */}
          <div className="mb-4 flex items-center gap-4">
            <select className="px-4 py-2 bg-white border border-gray-300 rounded-lg">
              <option value="">choose a prog language</option>
              <option value="c++">C++</option>
              <option value="python">Python</option>
              <option value="java">Java</option>
            </select>
            <button className="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700">Run</button>
            <button className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">Submit</button>
          </div>

          {/* Code editor section */}
          <div className="border-2 border-gray-300 rounded-lg p-4">
            <div className="bg-white">
              <pre className="text-gray-800 font-mono text-sm">
                <code>{`
#include<iostream>
#include<algorithm>
using namespace std
int codingfunction(){
}
int main(){}
                `}</code>
              </pre>
            </div>

            {/* Ved Section */}
            <div className="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-lg">
              <div className="font-medium mb-2">Ved</div>
              <p className="text-sm text-gray-700">
                here Ved will analyze the code and will suggest optimized code, user can ask any question<br/>
                <span className="text-blue-600">OpenAI is used for it</span>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PracticePage;