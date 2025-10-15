import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Progress } from '../../components/ui/Progress';
import { Button } from '../../components/ui/Button';
import { Home as HomeIcon, BookText, FileText, Cpu } from 'lucide-react';

const ProgressPage = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showUserMenu, setShowUserMenu] = useState(false);
  
  // Mock data for progress
  const [progressData, setProgressData] = useState({
    computerNetworks: 78,
    operatingSystem: 65,
    dataStructureAlgorithms: 78,
    oops: 100
  });

  const handleStartTest = (testDay) => {
    console.log(`Starting ${testDay} test`);
    // Navigate to test page or implement test functionality
  };

  const handleNavigation = (path) => {
    navigate(path);
  };

  const toggleUserMenu = () => {
    setShowUserMenu(!showUserMenu);
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-500 to-purple-600" style={{ backgroundImage: "url('/images/backme.svg')", backgroundSize: "cover", backgroundPosition: "center" }}>
      {/* Header with horizontal navigation */}
      <header className="bg-blue-600 p-4 flex justify-between items-center">
        <div className="flex space-x-8">
          <button 
            onClick={() => navigate('/dashboard')} 
            className="text-white flex items-center"
          >
            <HomeIcon className="h-4 w-4 mr-2" />
            <span>Home</span>
          </button>
          <button 
            onClick={() => navigate('/practice')} 
            className="text-white flex items-center"
          >
            <BookText className="h-4 w-4 mr-2" />
            <span>Practice</span>
          </button>
          <button 
            onClick={() => navigate('/resources')} 
            className="text-white flex items-center"
          >
            <FileText className="h-4 w-4 mr-2" />
            <span>Resource</span>
          </button>
          <button 
            onClick={() => navigate('/ved')} 
            className="text-white flex items-center"
          >
            <Cpu className="h-4 w-4 mr-2" />
            <span>Ved</span>
          </button>
        </div>
        
        <div className="relative">
          <button onClick={toggleUserMenu} className="bg-white rounded-full w-8 h-8 flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
          </button>
          
          {showUserMenu && (
            <div className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 z-10">
              <a href="#" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Profile</a>
              <a href="#" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Contact Us</a>
              <a href="#" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">About Us</a>
              <a href="#" onClick={() => navigate('/login')} className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Log Out</a>
            </div>
          )}
        </div>
      </header>

      {/* Main Content */}
      <div className="container mx-auto px-4 py-6">

        <div className="bg-white rounded-lg shadow-md p-6 max-w-6xl mx-auto">
          <h2 className="text-2xl font-bold text-gray-800 mb-6">Your Progress</h2>
          
          <div className="space-y-6">
            <div>
              <div className="flex justify-between mb-2">
                <h3 className="text-lg font-medium text-gray-700">Computer Networks</h3>
                <span className="text-sm font-medium text-blue-600">{progressData.computerNetworks}%</span>
              </div>
              <Progress value={progressData.computerNetworks} className="h-2" />
            </div>
            
            <div>
              <div className="flex justify-between mb-2">
                <h3 className="text-lg font-medium text-gray-700">Operating System</h3>
                <span className="text-sm font-medium text-blue-600">{progressData.operatingSystem}%</span>
              </div>
              <Progress value={progressData.operatingSystem} className="h-2" />
            </div>
            
            <div>
              <div className="flex justify-between mb-2">
                <h3 className="text-lg font-medium text-gray-700">Data Structure & Algorithms</h3>
                <span className="text-sm font-medium text-blue-600">{progressData.dataStructureAlgorithms}%</span>
              </div>
              <Progress value={progressData.dataStructureAlgorithms} className="h-2" />
            </div>
            
            <div>
              <div className="flex justify-between mb-2">
                <h3 className="text-lg font-medium text-gray-700">OOPs</h3>
                <span className="text-sm font-medium text-blue-600">{progressData.oops}%</span>
              </div>
              <Progress value={progressData.oops} className="h-2" />
            </div>
          </div>
          
          <div className="mt-10">
            <h3 className="text-xl font-bold text-gray-800 mb-4">Mock Tests</h3>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <Button 
                onClick={() => handleStartTest('Day 1')} 
                className="bg-blue-600 hover:bg-blue-700 text-white"
              >
                Day 1 Test
              </Button>
              
              <Button 
                onClick={() => handleStartTest('Day 2')} 
                className="bg-blue-600 hover:bg-blue-700 text-white"
              >
                Day 2 Test
              </Button>
              
              <Button 
                onClick={() => handleStartTest('Day 3')} 
                className="bg-blue-600 hover:bg-blue-700 text-white"
              >
                Day 3 Test
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProgressPage;