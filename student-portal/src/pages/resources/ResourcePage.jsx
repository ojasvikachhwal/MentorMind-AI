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

const ResourcePage = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const user = getCurrentUser();
  const [showUserMenu, setShowUserMenu] = useState(false);
  
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
      {/* Side navigation sidebar with purple gradient background */}
      <div 
        className="w-80 min-h-screen flex flex-col"
        style={{
          background: 'linear-gradient(180deg, #A855F7 0%, #7C3AED 100%)'
        }}
      >
        {/* Hamburger menu icon */}
        <div className="p-6">
          <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </div>

        {/* Navigation buttons - matching exact design */}
        <div className="px-6 space-y-3">
          {/* Home */}
          <div 
            className="flex items-center px-4 py-3 rounded-lg cursor-pointer hover:bg-white hover:bg-opacity-20 transition-colors"
            style={{
              backgroundColor: location.pathname === '/dashboard' ? '#f97316' : 'rgba(255,255,255,0.1)',
              borderColor: location.pathname === '/dashboard' ? '#f97316' : 'transparent',
              borderWidth: '2px'
            }}
            onClick={() => handleNavigation('dashboard')}
          >
            <HomeIcon className="w-5 h-5 text-white mr-3" />
            <span className="text-white font-medium">Home</span>
          </div>

          {/* Practice */}
          <div 
            className="flex items-center px-4 py-3 rounded-lg cursor-pointer hover:bg-white hover:bg-opacity-20 transition-colors"
            style={{
              backgroundColor: location.pathname === '/practice' ? '#f97316' : 'rgba(255,255,255,0.1)',
              borderColor: location.pathname === '/practice' ? '#f97316' : 'transparent',
              borderWidth: '2px'
            }}
            onClick={() => handleNavigation('practice')}
          >
            <BookText className="w-5 h-5 text-white mr-3" />
            <span className="text-white font-medium">Practice</span>
          </div>

          {/* Resource - Active */}
          <div 
            className="flex items-center px-4 py-3 rounded-lg cursor-pointer"
            style={{
              backgroundColor: location.pathname === '/resources' ? '#f97316' : 'rgba(255,255,255,0.1)',
              borderColor: location.pathname === '/resources' ? '#f97316' : 'transparent',
              borderWidth: '2px'
            }}
            onClick={() => handleNavigation('resources')}
          >
            <FileText className="w-5 h-5 text-white mr-3" />
            <span className="text-white font-medium">Resource</span>
          </div>

          {/* AI VED */}
          <div 
            className="flex items-center px-4 py-3 rounded-lg cursor-pointer hover:bg-white hover:bg-opacity-20 transition-colors"
            style={{
              backgroundColor: location.pathname === '/ved' ? '#f97316' : 'rgba(255,255,255,0.1)',
              borderColor: location.pathname === '/ved' ? '#f97316' : 'transparent',
              borderWidth: '2px'
            }}
            onClick={() => handleNavigation('ved')}
          >
            <div className="w-5 h-5 flex items-center justify-center mr-3">
              <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4"/>
              </svg>
            </div>
            <span className="text-white font-medium">AI VED</span>
          </div>
        </div>
      </div>

      {/* Main Content Area - RESOURCE CONTENT */}
      <div className="flex-1 min-h-screen bg-white">
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

        {/* Page Content - RECOMMENDED COURSES */}
        <div className="p-8">
          {/* Recommended courses section */}
          <div 
            className="inline-block px-6 py-3 rounded-lg text-white font-medium text-lg mb-6"
            style={{
              background: 'linear-gradient(90deg, #9333EA 0%, #3B82F6 100%)'
            }}
          >
            Recommended Courses
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Computer Networks */}
            <div className="border border-gray-200 rounded-lg shadow-sm p-6">
              <div className="flex items-center justify-between mb-4">
                <div 
                  className="px-4 py-2 rounded-lg text-sm font-medium"
                  style={{ backgroundColor: '#E1E4E8' }}
                >
                  ComputerNetworks
                </div>
              </div>
              <div className="text-sm text-gray-600">
                <div className="text-xs text-gray-500">Course ID</div>
                <div className="font-medium mb-2">CSE101-Computer Networks I</div>
                <div className="text-xs text-gray-500">Course Name</div>
                <div className="font-medium mb-2">Introduction to OSI Model</div>
                <div className="text-xs text-gray-500">Duration</div>
                <div className="font-medium mb-2">8 weeks</div>
                <div className="text-xs text-gray-500">Rating</div>
                <div className="flex items-center">
                  <div className="font-medium">4.8/5</div>
                  <div className="ml-2 flex">
                    {'★★★★★'.split('').map((star, i) => (
                      <span key={i} className="text-yellow-400 text-sm">{star}</span>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            {/* Operating System */}
            <div className="border border-gray-200 rounded-lg shadow-sm p-6">
              <div className="flex items-center justify-between mb-4">
                <div 
                  className="px-4 py-2 rounded-lg text-sm font-medium"
                  style={{ backgroundColor: '#E1E4E8' }}
                >
                  Operating System
                </div>
              </div>
              <div className="text-sm text-gray-600">
                <div className="text-xs text-gray-500">Course ID</div>
                <div className="font-medium mb-2">CSE102-OS Principles</div>
                <div className="text-xs text-gray-500">Course Name</div>
                <div className="font-medium mb-2">Memory Management & Processes</div>
                <div className="text-xs text-gray-500">Duration</div>
                <div className="font-medium mb-2">10 weeks</div>
                <div className="text-xs text-gray-500">Rating</div>
                <div className="flex items-center">
                  <div className="font-medium">4.9/5</div>
                  <div className="ml-2 flex">
                    {'★★★★★'.split('').map((star, i) => (
                      <span key={i} className="text-yellow-400 text-sm">{star}</span>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            {/* Data Structure & Algorithms */}
            <div className="border border-gray-200 rounded-lg shadow-sm p-6">
              <div className="flex items-center justify-between mb-4">
                <div 
                  className="px-4 py-2 rounded-lg text-sm font-medium"
                  style={{ backgroundColor: '#E1E4E8' }}
                >
                  Data Structure & Algorithms
                </div>
              </div>
              <div className="text-sm text-gray-600">
                <div className="text-xs text-gray-500">Course ID</div>
                <div className="font-medium mb-2">CSE201-Data Structures</div>
                <div className="text-xs text-gray-500">Course Name</div>
                <div className="font-medium mb-2">Arrays, Stacks & Queues</div>
                <div className="text-xs text-gray-500">Duration</div>
                <div className="font-medium mb-2">6 weeks</div>
                <div className="text-xs text-gray-500">Rating</div>
                <div className="flex items-center">
                  <div className="font-medium">4.7/5</div>
                  <div className="ml-2 flex">
                    {'★★★★★'.split('').map((star, i) => (
                      <span key={i} className="text-yellow-400 text-sm">{star}</span>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            {/* OOPS */}
            <div className="border border-gray-200 rounded-lg shadow-sm p-6">
              <div className="flex items-center justify-between mb-4">
                <div 
                  className="px-4 py-2 rounded-lg text-sm font-medium"
                  style={{ backgroundColor: '#E1E4E8' }}
                >
                  OOPS
                </div>
              </div>
              <div className="text-sm text-gray-600">
                <div className="text-xs text-gray-500">Course ID</div>
                <div className="font-medium mb-2">CSE301-Object-Oriented Programming</div>
                <div className="text-xs text-gray-500">Course Name</div>
                <div className="font-medium mb-2">Classes, Inheritance & Polymorphism</div>
                <div className="text-xs text-gray-500">Duration</div>
                <div className="font-medium mb-2">12 weeks</div>
                <div className="text-xs text-gray-500">Rating</div>
                <div className="flex items-center">
                  <div className="font-medium">4.9/5</div>
                  <div className="ml-2 flex">
                    {'★★★★★'.split('').map((star, i) => (
                      <span key={i} className="text-yellow-400 text-sm">{star}</span>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResourcePage;