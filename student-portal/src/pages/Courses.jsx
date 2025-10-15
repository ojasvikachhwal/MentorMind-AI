import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import ProfileDropdown from '../components/ProfileDropdown';

const Courses = () => {
  const [coursesData, setCoursesData] = useState({});
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');

  // Fallback data for development
  const fallbackData = {
    "Computer Networks": [
      {
        "title": "Introduction to Computer Networking",
        "platform": "Coursera",
        "url": "https://www.coursera.org/learn/computer-networking"
      },
      {
        "title": "Network Fundamentals",
        "platform": "Cisco Networking Academy",
        "url": "https://www.netacad.com/courses/networking/network-fundamentals"
      },
      {
        "title": "Computer Networks Course by NPTEL",
        "platform": "NPTEL",
        "url": "https://nptel.ac.in/courses/106105183"
      },
      {
        "title": "Networking Basics for Developers",
        "platform": "Udemy",
        "url": "https://www.udemy.com/course/networking-basics-for-developers/"
      }
    ],
    "Operating System": [
      {
        "title": "Operating Systems and You",
        "platform": "Coursera",
        "url": "https://www.coursera.org/learn/os-power-user"
      },
      {
        "title": "Introduction to OS Concepts",
        "platform": "NPTEL",
        "url": "https://nptel.ac.in/courses/106106144"
      },
      {
        "title": "Linux for Beginners",
        "platform": "Udemy",
        "url": "https://www.udemy.com/course/linux-for-beginners/"
      }
    ],
    "Data Structures & Algorithms": [
      {
        "title": "Mastering Data Structures and Algorithms",
        "platform": "Udemy",
        "url": "https://www.udemy.com/course/datastructurescncpp/"
      },
      {
        "title": "Data Structures and Algorithms Specialization",
        "platform": "Coursera",
        "url": "https://www.coursera.org/specializations/data-structures-algorithms"
      },
      {
        "title": "DSA through C++",
        "platform": "GeeksforGeeks",
        "url": "https://www.geeksforgeeks.org/courses/dsa-to-development-cpp"
      }
    ],
    "OOPS": [
      {
        "title": "Object Oriented Programming in Java",
        "platform": "Coursera",
        "url": "https://www.coursera.org/learn/object-oriented-java"
      },
      {
        "title": "C++ OOP Fundamentals",
        "platform": "Udemy",
        "url": "https://www.udemy.com/course/cpp-deep-dive/"
      },
      {
        "title": "OOPs Concepts in Python",
        "platform": "freeCodeCamp",
        "url": "https://www.freecodecamp.org/news/object-oriented-programming-in-python/"
      }
    ]
  };

  useEffect(() => {
    const fetchCourses = async () => {
      try {
        setLoading(true);
        // Try to fetch from API first
        const response = await fetch('/api/courses');
        if (response.ok) {
          const data = await response.json();
          setCoursesData(data);
        } else {
          // Use fallback data if API is not available
          setCoursesData(fallbackData);
        }
      } catch (error) {
        console.log('Using fallback data:', error);
        setCoursesData(fallbackData);
      } finally {
        setLoading(false);
      }
    };

    fetchCourses();
  }, []);

  const filteredCourses = (courses) => {
    if (!searchQuery) return courses;
    return courses.filter(course => 
      course.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      course.platform.toLowerCase().includes(searchQuery.toLowerCase())
    );
  };

  const subjects = Object.keys(coursesData);

  return (
    <div className="courses-page">
      <div className="main-content">
        {/* Header */}
        <div className="header">
          <h1 className="page-title">Recommended Courses</h1>
          <ProfileDropdown />
        </div>

        {/* Search Bar */}
        <div className="search-section">
          <input
            type="text"
            placeholder="Search for a course…"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="search-input"
          />
        </div>

        {/* Loading State */}
        {loading && (
          <div className="loading-container">
            <div className="loading-spinner"></div>
            <p>Fetching courses…</p>
          </div>
        )}

        {/* Courses Content */}
        {!loading && (
          <div className="courses-content">
            {subjects.map((subject, subjectIndex) => {
              const courses = filteredCourses(coursesData[subject]);
              
              return (
                <motion.div
                  key={subject}
                  className="subject-section"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: subjectIndex * 0.1 }}
                >
                  {/* Subject Heading */}
                  <div className="subject-heading">
                    {subject}
                  </div>

                  {/* Courses Grid */}
                  {courses.length > 0 ? (
                    <div className="courses-grid">
                      {courses.map((course, courseIndex) => (
                        <motion.div
                          key={courseIndex}
                          className="course-card"
                          initial={{ opacity: 0, scale: 0.9 }}
                          animate={{ opacity: 1, scale: 1 }}
                          transition={{ delay: (subjectIndex * 0.1) + (courseIndex * 0.05) }}
                          whileHover={{ scale: 1.05 }}
                          onClick={() => window.open(course.url, '_blank')}
                        >
                          <h3 className="course-title">{course.title}</h3>
                          <p className="course-platform">{course.platform}</p>
                        </motion.div>
                      ))}
                    </div>
                  ) : (
                    <p className="empty-state">
                      No courses available for this category yet.
                    </p>
                  )}
                </motion.div>
              );
            })}
          </div>
        )}
      </div>

      <style jsx>{`
        .courses-page {
          display: flex;
          min-height: 100vh;
          background-color: #ffffff;
          font-family: 'Inter', sans-serif;
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
          font-size: 2rem;
          font-weight: bold;
          background: linear-gradient(135deg, #3b82f6, #9333ea);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
        }

        .search-section {
          margin-bottom: 2rem;
        }

        .search-input {
          width: 100%;
          max-width: 400px;
          padding: 0.75rem 1rem;
          border: 1px solid #d1d5db;
          border-radius: 9999px;
          font-size: 0.875rem;
          transition: border-color 0.2s;
        }

        .search-input:focus {
          outline: none;
          border-color: #9333ea;
        }

        .loading-container {
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          padding: 4rem;
        }

        .loading-spinner {
          width: 40px;
          height: 40px;
          border: 4px solid #f3f4f6;
          border-top: 4px solid #7B2FF7;
          border-radius: 50%;
          animation: spin 1s linear infinite;
          margin-bottom: 1rem;
        }

        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }

        .courses-content {
          display: flex;
          flex-direction: column;
          gap: 2rem;
        }

        .subject-section {
          margin-bottom: 1.5rem;
        }

        .subject-heading {
          background-color: #E5D0FF;
          padding: 0.75rem 1rem;
          border-radius: 0.75rem;
          font-weight: 600;
          color: #374151;
          font-size: 1.125rem;
          margin-bottom: 1rem;
        }

        .courses-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
          gap: 1.5rem;
        }

        .course-card {
          background: white;
          border: 1px solid #E5E7EB;
          border-radius: 0.75rem;
          padding: 1rem;
          cursor: pointer;
          transition: all 0.2s ease;
          box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
          height: 140px;
          display: flex;
          flex-direction: column;
          justify-content: space-between;
        }

        .course-card:hover {
          border-color: #9333ea;
          color: #9333ea;
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }

        .course-title {
          font-size: 1rem;
          font-weight: 600;
          color: #374151;
          margin: 0 0 0.5rem 0;
          line-height: 1.4;
        }

        .course-card:hover .course-title {
          color: #9333ea;
        }

        .course-platform {
          font-size: 0.875rem;
          color: #6b7280;
          margin: 0;
        }

        .course-card:hover .course-platform {
          color: #9333ea;
        }

        .empty-state {
          color: #6b7280;
          font-style: italic;
          text-align: center;
          padding: 2rem;
        }

        /* Responsive Design */
        @media (max-width: 768px) {
          .main-content {
            margin-left: 60px;
            padding: 1rem;
          }

          .courses-grid {
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1rem;
          }

          .header {
            flex-direction: column;
            gap: 1rem;
            align-items: flex-start;
          }

          .page-title {
            font-size: 1.5rem;
          }
        }

        @media (max-width: 480px) {
          .main-content {
            margin-left: 0;
            padding: 1rem;
          }

          .courses-grid {
            grid-template-columns: 1fr;
          }

          .course-card {
            height: auto;
            min-height: 120px;
          }
        }
      `}</style>
    </div>
  );
};

export default Courses;
