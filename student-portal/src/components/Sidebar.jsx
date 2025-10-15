import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Menu, Home, Edit3, Package, Brain, BookOpen, ClipboardList } from 'lucide-react';

const Sidebar = ({ isOpen, setIsOpen }) => {
  const navigate = useNavigate();
  const location = useLocation();

  const sidebarItems = [
    { icon: Home, label: 'Home', path: '/dashboard' },
    { icon: Edit3, label: 'Practice', path: '/practice' },
    { icon: Package, label: 'Resource', path: '/courses' },
    { icon: Brain, label: 'VED', path: '/ved' },
    { icon: ClipboardList, label: 'Mock Tests', path: '/automated-mock-tests' }
  ];

  const handleNavigation = (path) => {
    navigate(path);
  };

  return (
    <motion.div 
      className={`sidebar ${isOpen ? 'sidebar-open' : 'sidebar-collapsed'}`}
      initial={{ x: -250 }}
      animate={{ x: 0 }}
      transition={{ duration: 0.3 }}
    >
      {/* Hamburger Menu */}
      <div className="sidebar-header">
        <button 
          className="hamburger-btn"
          onClick={() => setIsOpen(!isOpen)}
        >
          <Menu size={20} />
        </button>
      </div>

      {/* Sidebar Items */}
      <div className="sidebar-items">
        {sidebarItems.map((item, index) => {
          const IconComponent = item.icon;
          const isActive = location.pathname === item.path;
          
          return (
            <motion.button
              key={index}
              className={`sidebar-item ${isActive ? 'active' : ''}`}
              onClick={() => handleNavigation(item.path)}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              <IconComponent size={20} />
              {isOpen && <span>{item.label}</span>}
            </motion.button>
          );
        })}
      </div>

      <style jsx>{`
        .sidebar {
          width: 250px;
          background: linear-gradient(to bottom, #7B2FF7, #F107A3);
          color: white;
          position: fixed;
          height: 100vh;
          z-index: 1000;
          transition: all 0.3s ease;
          left: 0;
          top: 0;
        }

        .sidebar-collapsed {
          width: 60px;
        }

        .sidebar-header {
          padding: 1rem;
          border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }

        .hamburger-btn {
          background: none;
          border: none;
          color: white;
          cursor: pointer;
          padding: 0.5rem;
          border-radius: 0.5rem;
          transition: background-color 0.2s;
        }

        .hamburger-btn:hover {
          background-color: rgba(255, 255, 255, 0.1);
        }

        .sidebar-items {
          padding: 1rem 0.5rem;
        }

        .sidebar-item {
          display: flex;
          align-items: center;
          gap: 0.75rem;
          width: 100%;
          padding: 0.75rem 1rem;
          margin: 0.5rem 0;
          background: none;
          border: none;
          color: white;
          border-radius: 0.75rem;
          cursor: pointer;
          transition: all 0.2s ease;
          font-size: 0.875rem;
          font-weight: 500;
        }

        .sidebar-item:hover {
          background-color: #F5B6FF;
          color: black;
        }

        .sidebar-item.active {
          background-color: #F5B6FF;
          color: black;
          border: 2px solid #FF78C4;
        }

        /* Responsive Design */
        @media (max-width: 768px) {
          .sidebar {
            width: 60px;
          }

          .sidebar-item span {
            display: none;
          }
        }

        @media (max-width: 480px) {
          .sidebar {
            transform: translateX(-100%);
          }

          .sidebar-open {
            transform: translateX(0);
          }
        }
      `}</style>
    </motion.div>
  );
};

export default Sidebar;
