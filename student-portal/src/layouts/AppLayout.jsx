import React, { useState } from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from '../components/Sidebar';

const AppLayout = () => {
  const [sidebarOpen, setSidebarOpen] = useState(true);

  return (
    <div className="app-layout">
      <Sidebar isOpen={sidebarOpen} setIsOpen={setSidebarOpen} />
      <div className={`main-content-wrapper ${sidebarOpen ? 'sidebar-open' : 'sidebar-collapsed'}`}>
        <Outlet />
      </div>
      
      <style jsx>{`
        .app-layout {
          display: flex;
          min-height: 100vh;
          background-color: #ffffff;
        }

        .main-content-wrapper {
          flex: 1;
          margin-left: 250px;
          transition: margin-left 0.3s ease;
          min-height: 100vh;
          background-color: #ffffff;
        }

        .main-content-wrapper.sidebar-collapsed {
          margin-left: 60px;
        }

        /* Responsive Design */
        @media (max-width: 768px) {
          .main-content-wrapper {
            margin-left: 60px;
          }
          
          .main-content-wrapper.sidebar-open {
            margin-left: 60px;
          }
        }

        @media (max-width: 480px) {
          .main-content-wrapper {
            margin-left: 0;
          }
          
          .main-content-wrapper.sidebar-open {
            margin-left: 0;
          }
        }
      `}</style>
    </div>
  );
};

export default AppLayout;
