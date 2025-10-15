import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { BookOpen, TrendingUp, Clock, CheckCircle } from 'lucide-react';
import ProfileDropdown from '../../components/ProfileDropdown';

const Dashboard = () => {
  const [progressData, setProgressData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStudentProgress();
  }, []);

  const loadStudentProgress = async () => {
    try {
      const response = await fetch('/api/v1/automated-tests/progress/all', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      if (response.ok) {
        const data = await response.json();
        setProgressData(data);
      } else {
        console.error('Failed to load progress:', response.status, response.statusText);
        // Initialize with empty progress for new users
        setProgressData([]);
      }
    } catch (error) {
      console.error('Failed to load progress:', error);
      // Initialize with empty progress for new users
      setProgressData([]);
    } finally {
      setLoading(false);
    }
  };

  const handleStartTest = () => {
    // Navigate to automated mock tests page
    window.location.href = '/automated-mock-tests';
  };

  const getProgressColor = (percentage) => {
    if (percentage >= 80) return '#10B981'; // green
    if (percentage >= 60) return '#F59E0B'; // yellow
    if (percentage >= 40) return '#EF4444'; // red
    return '#6B7280'; // gray
  };

  const getProgressLabel = (percentage) => {
    if (percentage >= 80) return 'Excellent';
    if (percentage >= 60) return 'Good';
    if (percentage >= 40) return 'Needs Improvement';
    return 'Beginner';
  };


  return (
    <div className="dashboard">
      {/* Main Content */}
      <div className="main-content">
        {/* Header */}
        <div className="header">
          <h1 className="page-title">Progress</h1>
          <ProfileDropdown />
        </div>

        {/* Progress Section */}
        <div className="progress-section">
          <h2 className="section-title">Subject Progress</h2>
          {loading ? (
            <div className="loading-container">
              <div className="loading-spinner"></div>
              <p>Loading progress...</p>
            </div>
          ) : progressData.length === 0 ? (
            <div className="empty-state">
              <BookOpen className="w-16 h-16 text-gray-300 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">No Progress Yet</h3>
              <p className="text-gray-500 mb-4">Start taking automated mock tests to see your progress here.</p>
              <button
                onClick={handleStartTest}
                className="px-6 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
              >
                Take Your First Test
              </button>
            </div>
          ) : (
            <div className="progress-items">
              {progressData.map((item, index) => (
                <motion.div
                  key={item.subject_id}
                  className="progress-item"
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1 }}
                >
                  <div className="progress-header">
                    <div className="progress-label">
                      <span className="label-text">{item.subject_name}</span>
                      <span className="progress-status">{getProgressLabel(item.progress_percentage)}</span>
                    </div>
                    <div className="progress-metrics">
                      <span className="percentage" style={{ color: getProgressColor(item.progress_percentage) }}>
                        {item.progress_percentage.toFixed(1)}%
                      </span>
                    </div>
                  </div>
                  
                  <div className="progress-stats">
                    <div className="stat">
                      <CheckCircle className="w-4 h-4 text-green-600" />
                      <span>{item.total_tests_taken} tests taken</span>
                    </div>
                    <div className="stat">
                      <TrendingUp className="w-4 h-4 text-blue-600" />
                      <span>Best: {item.best_score.toFixed(1)}%</span>
                    </div>
                    <div className="stat">
                      <Clock className="w-4 h-4 text-purple-600" />
                      <span>Avg: {item.average_score.toFixed(1)}%</span>
                    </div>
                  </div>
                  
                  <div className="progress-bar-container">
                    <motion.div
                      className="progress-bar-fill"
                      style={{ backgroundColor: getProgressColor(item.progress_percentage) }}
                      initial={{ width: 0 }}
                      animate={{ width: `${item.progress_percentage}%` }}
                      transition={{ duration: 1, delay: index * 0.2 }}
                    />
                  </div>
                </motion.div>
              ))}
            </div>
          )}
        </div>

        {/* Mock Test Section */}
        <div className="mock-test-section">
          <h2 className="section-title">Automated Mock Tests</h2>
          <div className="mock-test-cards">
            <motion.div
              className="mock-test-card"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 }}
              whileHover={{ scale: 1.02 }}
            >
              <div className="test-header">
                <BookOpen className="w-8 h-8 text-purple-600" />
                <h3 className="test-title">AI-Generated Tests</h3>
              </div>
              <p className="test-description">
                Take personalized mock tests generated by AI based on your progress in each subject.
              </p>
              <div className="test-features">
                <div className="feature">
                  <CheckCircle className="w-4 h-4 text-green-600" />
                  <span>Adaptive difficulty</span>
                </div>
                <div className="feature">
                  <TrendingUp className="w-4 h-4 text-blue-600" />
                  <span>Progress tracking</span>
                </div>
                <div className="feature">
                  <Clock className="w-4 h-4 text-purple-600" />
                  <span>Instant evaluation</span>
                </div>
              </div>
              <motion.button
                className="start-btn"
                onClick={handleStartTest}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                Start Test
              </motion.button>
            </motion.div>
          </div>
        </div>
        </div>
        
      <style jsx>{`
        .dashboard {
          display: flex;
          min-height: 100vh;
          background-color: #ffffff;
        }

        .sidebar {
          width: 250px;
          background: linear-gradient(180deg, #7B2FF7 0%, #F107A3 100%);
          color: white;
          position: fixed;
          height: 100vh;
          z-index: 1000;
          transition: all 0.3s ease;
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

        .main-content {
          flex: 1;
          margin-left: 250px;
          padding: 2rem;
          background-color: #ffffff;
          transition: margin-left 0.3s ease;
        }

        .sidebar-collapsed + .main-content {
          margin-left: 60px;
        }

        .header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 2rem;
        }

        .page-title {
          font-size: 1.5rem;
          font-weight: bold;
          background: linear-gradient(135deg, #3b82f6, #9333ea);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
        }

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
          background-color: #f3f4f6;
        }

        .dropdown-item:first-child {
          border-radius: 0.5rem 0.5rem 0 0;
        }

        .dropdown-item:last-child {
          border-radius: 0 0 0.5rem 0.5rem;
        }

        .progress-section {
          margin-bottom: 2rem;
        }

        .section-title {
          font-size: 1.25rem;
          font-weight: bold;
          background: linear-gradient(135deg, #3b82f6, #9333ea);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
          margin-bottom: 1.5rem;
        }

        .progress-items {
          display: flex;
          flex-direction: column;
          gap: 1.25rem;
        }

        .loading-container {
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          padding: 3rem;
          color: #6B7280;
        }

        .loading-spinner {
          width: 40px;
          height: 40px;
          border: 4px solid #E5E7EB;
          border-top: 4px solid #7B2FF7;
          border-radius: 50%;
          animation: spin 1s linear infinite;
          margin-bottom: 1rem;
        }

        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }

        .empty-state {
          text-align: center;
          padding: 3rem;
          color: #6B7280;
        }

        .progress-item {
          background-color: #F9FAFB;
          padding: 1.5rem;
          border-radius: 0.75rem;
          border: 1px solid #E5E7EB;
          margin-bottom: 1rem;
        }

        .progress-header {
          display: flex;
          justify-content: space-between;
          align-items: flex-start;
          margin-bottom: 1rem;
        }

        .progress-label {
          display: flex;
          flex-direction: column;
          gap: 0.25rem;
        }

        .label-text {
          font-weight: bold;
          font-size: 1rem;
          color: #374151;
        }

        .progress-status {
          font-size: 0.75rem;
          color: #6B7280;
          text-transform: uppercase;
          letter-spacing: 0.05em;
        }

        .progress-metrics {
          text-align: right;
        }

        .percentage {
          font-weight: bold;
          font-size: 1.25rem;
        }

        .progress-stats {
          display: flex;
          gap: 1rem;
          margin-bottom: 1rem;
          flex-wrap: wrap;
        }

        .stat {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          font-size: 0.875rem;
          color: #6B7280;
        }

        .progress-bar-container {
          width: 100%;
          height: 8px;
          background-color: #E5E7EB;
          border-radius: 9999px;
          overflow: hidden;
        }

        .progress-bar-fill {
          height: 100%;
          background-color: #EF4444;
          border-radius: 9999px;
          transition: width 1s ease;
        }

        .mock-test-section {
          margin-bottom: 2rem;
        }

        .mock-test-cards {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
          gap: 1rem;
        }

        .mock-test-card {
          background-color: #F9FAFB;
          padding: 1.5rem;
          border-radius: 0.75rem;
          border: 1px solid #E5E7EB;
          display: flex;
          flex-direction: column;
          gap: 1rem;
        }

        .test-header {
          display: flex;
          align-items: center;
          gap: 0.75rem;
          margin-bottom: 0.5rem;
        }

        .test-title {
          font-size: 1.25rem;
          font-weight: 600;
          color: #374151;
          margin: 0;
        }

        .test-description {
          color: #6B7280;
          font-size: 0.875rem;
          line-height: 1.5;
          margin: 0;
        }

        .test-features {
          display: flex;
          flex-direction: column;
          gap: 0.5rem;
        }

        .feature {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          font-size: 0.875rem;
          color: #6B7280;
        }

        .start-btn {
          background: linear-gradient(135deg, #7B2FF7, #F107A3);
          color: white;
          border: none;
          border-radius: 0.5rem;
          padding: 0.5rem 1rem;
          font-weight: 500;
          cursor: pointer;
          transition: all 0.2s ease;
          align-self: flex-start;
        }

        .start-btn:hover {
          transform: scale(1.05);
        }

        /* Responsive Design */
        @media (max-width: 768px) {
          .sidebar {
            width: 60px;
          }

          .sidebar-item span {
            display: none;
          }

          .main-content {
            margin-left: 60px;
            padding: 1rem;
          }

          .mock-test-cards {
            grid-template-columns: 1fr;
          }

          .header {
            flex-direction: column;
            gap: 1rem;
            align-items: flex-start;
          }

          .profile-section {
            align-self: flex-end;
          }
        }

        @media (max-width: 480px) {
          .main-content {
            margin-left: 0;
            padding: 1rem;
          }

          .sidebar {
            transform: translateX(-100%);
          }

          .sidebar-open {
            transform: translateX(0);
          }

          .progress-item {
            padding: 0.75rem;
          }

          .mock-test-card {
            padding: 0.75rem;
          }
        }
      `}</style>
    </div>
  );
};

export default Dashboard;