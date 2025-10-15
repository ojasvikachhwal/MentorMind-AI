import React from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Button } from '../components/ui/Button';

const Home = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex flex-col bg-blue-600 bg-opacity-90">
      <div className="absolute inset-0 z-0">
        {/* Background with educational icons */}
        <div className="absolute top-20 left-20 w-12 h-12 rounded-full bg-blue-500 bg-opacity-50 flex items-center justify-center">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
          </svg>
        </div>
        <div className="absolute top-40 right-40 w-12 h-12 rounded-full bg-blue-500 bg-opacity-50 flex items-center justify-center">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
          </svg>
        </div>
        <div className="absolute bottom-40 left-40 w-12 h-12 rounded-full bg-blue-500 bg-opacity-50 flex items-center justify-center">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
          </svg>
        </div>
        <div className="absolute bottom-20 right-20 w-12 h-12 rounded-full bg-blue-500 bg-opacity-50 flex items-center justify-center">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
        </div>
      </div>

      {/* Header */}
      <header className="p-4 flex justify-between items-center z-10">
        <div className="text-white text-2xl font-bold">MENTORMIND-AI</div>
        <div className="space-x-4">
          <Button 
            variant="outline" 
            className="text-white border-white hover:bg-white hover:text-blue-600"
            onClick={() => navigate('/login')}
          >
            Log In
          </Button>
          <Button 
            className="bg-white text-blue-600 hover:bg-blue-100"
            onClick={() => navigate('/signup')}
          >
            Sign Up
          </Button>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-grow flex items-center justify-center z-10">
        <div className="max-w-3xl text-center px-4">
          <h1 className="text-4xl md:text-6xl font-bold text-white mb-6">Personalized Learning with AI</h1>
          <p className="text-xl text-white mb-8">Track your progress, practice with interactive exercises, and get personalized recommendations to improve your skills.</p>
          <div className="space-x-4">
            <Button 
              className="bg-white text-blue-600 hover:bg-blue-100 text-lg px-8 py-3"
              onClick={() => navigate('/signup')}
            >
              Get Started
            </Button>
            <Button 
              variant="outline" 
              className="text-white border-white hover:bg-white hover:text-blue-600 text-lg px-8 py-3"
              onClick={() => navigate('/login')}
            >
              Learn More
            </Button>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="p-4 text-center text-white text-sm z-10">
        <p>© 2023 MentorMind-AI. All rights reserved. | <Link to="/terms" className="hover:underline">Terms of Service</Link> | <Link to="/privacy" className="hover:underline">Privacy Policy</Link></p>
      </footer>
    </div>
  );
};

export default Home;