import React, { useState, useEffect } from 'react';
import { useNavigate, Outlet, Routes, Route } from 'react-router-dom';
import { 
  Menu, 
  X,
  Users,
  ClipboardList,
  GraduationCap,
  BarChart3,
  LogOut,
  Sun,
  Moon
} from 'lucide-react';
import Students from './Students';
import Assessments from './Assessments';
import Courses from './Courses';
import Reports from './Reports';

const AdminDashboard = () => {
  const navigate = useNavigate();
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [darkMode, setDarkMode] = useState(false);
  const [adminInfo, setAdminInfo] = useState(null);

  useEffect(() => {
    // Check if admin is authenticated
    const token = localStorage.getItem('adminToken');
    const admin = localStorage.getItem('adminInfo');
    
    if (!token || !admin) {
      navigate('/admin/login');
      return;
    }

    try {
      setAdminInfo(JSON.parse(admin));
    } catch (error) {
      console.error('Error parsing admin info:', error);
      navigate('/admin/login');
    }
  }, [navigate]);

  useEffect(() => {
    // Apply dark mode to body
    if (darkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [darkMode]);

  const handleLogout = () => {
    localStorage.removeItem('adminToken');
    localStorage.removeItem('adminInfo');
    navigate('/admin/login');
  };

  const navigation = [
    { name: 'Students', href: '/admin/students', icon: Users, current: true },
    { name: 'Assessments', href: '/admin/assessments', icon: ClipboardList, current: false },
    { name: 'Courses', href: '/admin/courses', icon: GraduationCap, current: false },
    { name: 'Reports', href: '/admin/reports', icon: BarChart3, current: false },
  ];

  const handleNavigation = (href) => {
    navigate(href);
    // Update current state for all navigation items
    navigation.forEach(item => {
      item.current = item.href === href;
    });
  };

  if (!adminInfo) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
        <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  return (
    <div className={`min-h-screen ${darkMode ? 'dark' : ''}`}>
      <div className="bg-gray-50 dark:bg-gray-900 min-h-screen">
        {/* Mobile sidebar */}
        <div className={`fixed inset-0 z-50 lg:hidden ${sidebarOpen ? 'block' : 'hidden'}`}>
          <div className="fixed inset-0 bg-gray-600 bg-opacity-75" onClick={() => setSidebarOpen(false)} />
          <div className="fixed inset-y-0 left-0 flex w-64 flex-col bg-white dark:bg-gray-800">
            <div className="flex h-16 items-center justify-between px-4">
              <h1 className="text-xl font-semibold text-gray-900 dark:text-white">MentorMind Admin</h1>
              <button
                onClick={() => setSidebarOpen(false)}
                className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
              >
                <X className="h-6 w-6" />
              </button>
            </div>
            <nav className="flex-1 space-y-1 px-2 py-4">
              {navigation.map((item) => (
                <button
                  key={item.name}
                  onClick={() => handleNavigation(item.href)}
                  className={`group flex items-center px-2 py-2 text-sm font-medium rounded-md w-full text-left ${
                    item.current
                      ? 'bg-indigo-100 text-indigo-900 dark:bg-indigo-900 dark:text-indigo-100'
                      : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900 dark:text-gray-300 dark:hover:bg-gray-700 dark:hover:text-white'
                  }`}
                >
                  <item.icon
                    className={`mr-3 h-5 w-5 flex-shrink-0 ${
                      item.current ? 'text-indigo-500' : 'text-gray-400 group-hover:text-gray-500'
                    }`}
                  />
                  {item.name}
                </button>
              ))}
            </nav>
          </div>
        </div>

        {/* Desktop sidebar */}
        <div className="hidden lg:fixed lg:inset-y-0 lg:flex lg:w-64 lg:flex-col">
          <div className="flex flex-col flex-grow bg-white dark:bg-gray-800 pt-5 pb-4 overflow-y-auto">
            <div className="flex items-center flex-shrink-0 px-4">
              <h1 className="text-xl font-semibold text-gray-900 dark:text-white">MentorMind Admin</h1>
            </div>
            <nav className="mt-8 flex-1 space-y-1 px-2">
              {navigation.map((item) => (
                <button
                  key={item.name}
                  onClick={() => handleNavigation(item.href)}
                  className={`group flex items-center px-2 py-2 text-sm font-medium rounded-md w-full text-left ${
                    item.current
                      ? 'bg-indigo-100 text-indigo-900 dark:bg-indigo-900 dark:text-indigo-100'
                      : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900 dark:text-gray-300 dark:hover:bg-gray-700 dark:hover:text-white'
                  }`}
                >
                  <item.icon
                    className={`mr-3 h-5 w-5 flex-shrink-0 ${
                      item.current ? 'text-indigo-500' : 'text-gray-400 group-hover:text-gray-500'
                    }`}
                  />
                  {item.name}
                </button>
              ))}
            </nav>
          </div>
        </div>

        {/* Main content */}
        <div className="lg:pl-64 flex flex-col flex-1">
          {/* Top bar */}
          <div className="sticky top-0 z-10 flex-shrink-0 flex h-16 bg-white dark:bg-gray-800 shadow">
            <button
              type="button"
              className="px-4 border-r border-gray-200 dark:border-gray-700 text-gray-500 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-indigo-500 lg:hidden"
              onClick={() => setSidebarOpen(true)}
            >
                              <Menu className="h-6 w-6" />
            </button>
            
            <div className="flex-1 px-4 flex justify-between">
              <div className="flex-1 flex">
                <h2 className="text-2xl font-semibold text-gray-900 dark:text-white my-auto">
                  Admin Dashboard
                </h2>
              </div>
              
              <div className="ml-4 flex items-center md:ml-6 space-x-4">
                {/* Dark mode toggle */}
                <button
                  onClick={() => setDarkMode(!darkMode)}
                  className="p-2 rounded-md text-gray-400 hover:text-gray-500 dark:hover:text-gray-300"
                >
                  {darkMode ? (
                    <Sun className="h-5 w-5" />
                  ) : (
                                          <Moon className="h-5 w-5" />
                  )}
                </button>

                {/* Admin info */}
                <div className="flex items-center space-x-3">
                  <div className="text-right">
                    <p className="text-sm font-medium text-gray-900 dark:text-white">
                      {adminInfo.username}
                    </p>
                    <p className="text-xs text-gray-500 dark:text-gray-400">
                      Administrator
                    </p>
                  </div>
                  <div className="h-8 w-8 rounded-full bg-indigo-600 flex items-center justify-center">
                    <span className="text-sm font-medium text-white">
                      {adminInfo.username.charAt(0).toUpperCase()}
                    </span>
                  </div>
                </div>

                {/* Logout button */}
                <button
                  onClick={handleLogout}
                  className="p-2 rounded-md text-gray-400 hover:text-gray-500 dark:hover:text-gray-300"
                  title="Logout"
                >
                  <LogOut className="h-5 w-5" />
                </button>
              </div>
            </div>
          </div>

          {/* Page content */}
          <main className="flex-1">
            <div className="py-6">
              <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <Routes>
                  <Route path="/" element={<Students />} />
                  <Route path="/students" element={<Students />} />
                  <Route path="/assessments" element={<Assessments />} />
                  <Route path="/courses" element={<Courses />} />
                  <Route path="/reports" element={<Reports />} />
                </Routes>
              </div>
            </div>
          </main>
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;
