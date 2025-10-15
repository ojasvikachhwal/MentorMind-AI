import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { signup } from '../../services/api';

const SignupPage = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSignUp = async (e) => {
    e.preventDefault();
    try {
      console.log('Signup attempt:', formData);
      const result = await signup(formData);
      console.log('Signup successful:', result);
      navigate('/dashboard');
    } catch (error) {
      console.error('Signup failed:', error);
      alert('Signup failed: ' + error.message);
    }
  };

  const handleGoogleSignUp = async () => {
    try {
      // TODO: Implement Google OAuth
    console.log('Google signup clicked');
      // For now, simulate a successful signup
      const mockCredentials = { email: 'google@example.com', password: 'google123' };
      const result = await signup(mockCredentials);
      console.log('Google signup successful:', result);
      navigate('/dashboard');
    } catch (error) {
      console.error('Google signup failed:', error);
      alert('Google signup failed: ' + error.message);
    }
  };

  const handleLoginClick = () => {
    navigate('/login');
  };

  return (
    <div className="signup-page">
      {/* Background with backme.png */}
      <div className="background-image"></div>
      
      {/* Dark overlay */}
      <div className="dark-overlay"></div>
      
      {/* Center Card */}
      <div className="center-card">
        {/* Heading */}
        <h1 className="heading">MENTORMIND-AI</h1>
        
        {/* Subheading */}
        <h2 className="subheading">Create an Account</h2>
        
        {/* Signup Form */}
        <form onSubmit={handleSignUp} className="form-container">
          {/* Email Input */}
                <input
                  type="email"
                  name="email"
            placeholder="email@domain.com"
                  value={formData.email}
            onChange={handleInputChange}
            className="input-field"
                  required
                />
              
          {/* Password Input */}
                <input
                  type="password"
                  name="password"
            placeholder="password"
                  value={formData.password}
            onChange={handleInputChange}
            className="input-field"
                  required
                />
          
          {/* Sign Up Button */}
          <button type="submit" className="main-button">
            Sign In
              </button>
            </form>
            
        {/* Divider */}
        <div className="divider">or Sign up by</div>
        
        {/* Google Signup Button */}
        <button onClick={handleGoogleSignUp} className="google-button">
          <svg className="google-icon" viewBox="0 0 24 24" width="16" height="16">
            <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
            <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
            <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
            <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
                </svg>
          Google
              </button>
        
        {/* Terms Text */}
        <p className="terms-text">
          By clicking continue, you agree to our terms and conditions.
        </p>
        
        {/* Bottom Link */}
        <button onClick={handleLoginClick} className="bottom-link">
          sign up or log in
        </button>
      </div>

      <style jsx>{`
        .signup-page {
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
          height: auto;
          background-color: rgba(255, 255, 255, 0.78);
          border-radius: 16px;
          box-shadow: 0 4px 30px rgba(0, 0, 0, 0.25);
          padding: 35px 40px;
          display: flex;
          flex-direction: column;
          align-items: center;
          backdrop-filter: blur(12px);
          transition: opacity 0.5s ease;
          animation: fadeIn 0.5s ease-in-out;
        }

        .heading {
          font-family: 'Poppins', sans-serif;
          font-size: 30px;
          font-weight: 600;
          color: #3b2b1c;
          letter-spacing: 2px;
          margin-bottom: 20px;
          text-align: center;
        }

        .subheading {
          font-size: 16px;
          color: #333333;
          margin-bottom: 15px;
          text-align: center;
        }

        .form-container {
          width: 100%;
          display: flex;
          flex-direction: column;
          align-items: center;
        }

        .input-field {
          width: 300px;
          height: 40px;
          border-radius: 8px;
          border: 1px solid #ccc;
          background: white;
          padding: 10px;
          font-size: 14px;
          color: #333;
          margin: 8px 0;
          transition: border-color 0.3s ease;
        }

        .input-field:focus {
          border-color: #2a6fdb;
          outline: none;
        }

        .main-button {
          width: 300px;
          height: 40px;
          background-color: #000000;
          color: #ffffff;
          font-size: 15px;
          font-weight: 500;
          border-radius: 20px;
          border: none;
          margin-top: 12px;
          cursor: pointer;
          transition: all 0.2s ease;
        }

        .main-button:hover {
          transform: scale(1.05);
          box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        }

        .divider {
          font-size: 13px;
          color: #444;
          margin: 18px 0;
          text-align: center;
        }

        .google-button {
          width: 140px;
          height: 38px;
          background: white;
          border: 1px solid #ccc;
          border-radius: 20px;
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 8px;
          cursor: pointer;
          transition: background 0.3s ease;
          margin-bottom: 15px;
          font-size: 14px;
        }

        .google-button:hover {
          background: #f3f3f3;
        }

        .google-icon {
          width: 16px;
          height: 16px;
        }

        .terms-text {
          font-size: 10px;
          color: #555;
          text-align: center;
          margin-top: 5px;
        }

        .bottom-link {
          font-size: 12px;
          color: #333;
          text-align: center;
          margin-top: 15px;
          background: none;
          border: none;
          cursor: pointer;
          text-decoration: underline;
          transition: color 0.3s ease;
        }

        .bottom-link:hover {
          color: #2a6fdb;
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
            padding: 25px 30px;
          }

          .heading {
            font-size: 26px;
          }

          .input-field,
          .main-button {
            width: 100%;
            max-width: 280px;
          }

          .google-button {
            width: 120px;
          }
        }

        @media (max-width: 480px) {
          .center-card {
            width: 95%;
            max-width: 350px;
            padding: 20px 25px;
          }

          .heading {
            font-size: 24px;
            letter-spacing: 1px;
          }

          .input-field,
          .main-button {
            width: 100%;
            max-width: 250px;
          }

          .google-button {
            width: 100px;
            font-size: 12px;
          }
        }
      `}</style>
    </div>
  );
};

export default SignupPage;