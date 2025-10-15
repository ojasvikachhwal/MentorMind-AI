import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { UserCircle, User, MessageCircle, Info, LogOut } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const ProfileDropdown = () => {
  const [isOpen, setIsOpen] = useState(false);
  const profileRef = useRef(null);
  const navigate = useNavigate();

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (profileRef.current && !profileRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  const handleProfileClick = () => {
    setIsOpen(!isOpen);
  };

  const handleLogout = () => {
    // Clear localStorage and redirect to login
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    navigate('/login');
  };

  const dropdownItems = [
    { icon: User, label: 'Profile', action: () => console.log('Profile clicked') },
    { icon: MessageCircle, label: 'Contact Us', action: () => console.log('Contact Us clicked') },
    { icon: Info, label: 'About Us', action: () => console.log('About Us clicked') },
    { icon: LogOut, label: 'Log Out', action: handleLogout }
  ];

  return (
    <div className="profile-section" ref={profileRef}>
      <motion.button
        className="profile-btn"
        onClick={handleProfileClick}
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
      >
        <UserCircle size={24} />
      </motion.button>

      {/* Profile Dropdown */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            className="profile-dropdown"
            initial={{ opacity: 0, y: -10, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -10, scale: 0.95 }}
            transition={{ duration: 0.2 }}
          >
            {dropdownItems.map((item, index) => {
              const IconComponent = item.icon;
              return (
                <button 
                  key={index}
                  className="dropdown-item"
                  onClick={item.action}
                >
                  <IconComponent size={16} />
                  {item.label}
                </button>
              );
            })}
          </motion.div>
        )}
      </AnimatePresence>

      <style jsx>{`
        .profile-section {
          position: relative;
        }

        .profile-btn {
          width: 48px;
          height: 48px;
          border-radius: 50%;
          background-color: #C6A8FF;
          border: none;
          cursor: pointer;
          display: flex;
          align-items: center;
          justify-content: center;
          color: white;
          transition: all 0.2s ease;
        }

        .profile-btn:hover {
          background-color: #B894FF;
        }

        .profile-dropdown {
          position: absolute;
          top: 100%;
          right: 0;
          margin-top: 0.5rem;
          background: white;
          border-radius: 0.5rem;
          box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
          border: 1px solid #e5e7eb;
          z-index: 1000;
          min-width: 150px;
        }

        .dropdown-item {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          width: 100%;
          padding: 0.75rem 1rem;
          background: none;
          border: none;
          color: #374151;
          cursor: pointer;
          transition: background-color 0.2s;
          font-size: 0.875rem;
        }

        .dropdown-item:hover {
          background-color: #E5D0FF;
        }

        .dropdown-item:first-child {
          border-radius: 0.5rem 0.5rem 0 0;
        }

        .dropdown-item:last-child {
          border-radius: 0 0 0.5rem 0.5rem;
        }
      `}</style>
    </div>
  );
};

export default ProfileDropdown;
