import React from 'react';
import { useNavigate } from 'react-router-dom';

const WelcomePage = () => {
  const navigate = useNavigate();

  const handleSignUp = () => {
    navigate('/signup');
  };

  const handleLogIn = () => {
    navigate('/login');
  };

  return (
    <div className="welcome-page">
      {/* Background with backme.png */}
      <div className="background-image"></div>
      
      {/* Dark overlay */}
      <div className="dark-overlay"></div>
      
      {/* Center Card */}
      <div className="center-card">
        {/* Title */}
        <h1 className="title">MENTORMIND-AI</h1>
        
        {/* Buttons Container */}
        <div className="buttons-container">
          <button 
            className="auth-button" 
            onClick={handleSignUp}
          >
            SIGN UP
          </button>
          <button 
            className="auth-button" 
            onClick={handleLogIn}
          >
            LOG IN
          </button>
        </div>
        
        {/* Subtext */}
        <p className="subtext">
          By clicking continue, you agree to our{' '}
          <a href="/terms" className="link">Terms of Service</a>
          {' '}and{' '}
          <a href="/privacy" className="link">Privacy Policy</a>.
        </p>
      </div>

      <style jsx>{`
        .welcome-page {
          position: relative;
          width: 100vw;
          height: 100vh;
          overflow: hidden;
          display: flex;
          align-items: center;
          justify-content: center;
        }

        .background-image {
          position: absolute;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          background-image: url('/backme.png');
          background-size: cover;
          background-position: center;
          background-repeat: no-repeat;
        }

        .dark-overlay {
          position: absolute;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          background-color: rgba(0, 0, 0, 0.3);
        }

        .center-card {
          position: relative;
          z-index: 10;
          width: 480px;
          height: 400px;
          background-color: rgba(255, 255, 255, 0.75);
          border-radius: 15px;
          box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          animation: fadeIn 1s ease-in-out;
          backdrop-filter: blur(10px);
        }

        .title {
          font-family: 'Poppins', sans-serif;
          font-size: 28px;
          font-weight: 600;
          color: #3b2b1c;
          text-align: center;
          letter-spacing: 2px;
          margin-top: 50px;
          margin-bottom: 40px;
        }

        .buttons-container {
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 20px;
          margin-bottom: 25px;
        }

        .auth-button {
          width: 160px;
          height: 45px;
          border-radius: 25px;
          border: none;
          background-color: white;
          color: #333;
          font-size: 14px;
          font-weight: 500;
          cursor: pointer;
          transition: all 0.3s ease;
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }

        .auth-button:hover {
          transform: scale(1.05);
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        }

        .subtext {
          font-size: 11px;
          color: #555;
          text-align: center;
          margin-top: 25px;
          line-height: 1.4;
        }

        .link {
          color: #2a6fdb;
          text-decoration: underline;
          cursor: pointer;
        }

        .link:hover {
          color: #1e5bb8;
        }

        @keyframes fadeIn {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        /* Responsive Design */
        @media (max-width: 768px) {
          .center-card {
            width: 90%;
            max-width: 400px;
            height: auto;
            min-height: 350px;
            padding: 20px;
            margin: 20px;
          }

          .title {
            font-size: 24px;
            margin-top: 30px;
            margin-bottom: 30px;
          }

          .auth-button {
            width: 140px;
            height: 40px;
            font-size: 13px;
          }
        }

        @media (max-width: 480px) {
          .center-card {
            width: 95%;
            max-width: 350px;
            min-height: 320px;
          }

          .title {
            font-size: 22px;
            letter-spacing: 1px;
          }

          .auth-button {
            width: 120px;
            height: 38px;
            font-size: 12px;
          }

          .subtext {
            font-size: 10px;
            padding: 0 10px;
          }
        }
      `}</style>
    </div>
  );
};

export default WelcomePage;
