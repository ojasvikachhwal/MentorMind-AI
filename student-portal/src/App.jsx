import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import ProtectedRoute from './components/ProtectedRoute';

// Home Page
import Home from './pages/Home';
import WelcomePage from './pages/WelcomePage';

// Layout
import AppLayout from './layouts/AppLayout';

// Auth Pages
import ForgotPassword from './pages/auth/ForgotPassword';
import ResetPassword from './pages/auth/ResetPassword';
import LoginPage from './pages/auth/LoginPage';
import SignupPage from './pages/auth/SignupPage';

// Dashboard
import Dashboard from './pages/dashboard/Dashboard';

// Assessment Pages
import SubjectSelection from './pages/assessment/SubjectSelection';
import AssessmentTest from './pages/assessment/AssessmentTest';
import AssessmentResults from './pages/assessment/AssessmentResults';

// Course Pages
import Recommendations from './pages/Recommendations';

// Progress Tracking Pages
import ProgressPage from './pages/progress/ProgressPage';

// New Pages
import PracticePage from './pages/practice/PracticePage';
import ResourcePage from './pages/resources/ResourcePage';
import VedPage from './pages/ved/VedPage';
import Courses from './pages/Courses';
import Practice from './pages/Practice';

// Mock Test Pages
import MockTestTaker from './pages/student/MockTestTaker';
import AutomatedMockTests from './pages/AutomatedMockTests';

// Admin Pages
import AdminLogin from './pages/admin/AdminLogin';
import AdminDashboard from './pages/admin/AdminDashboard';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          {/* Public Routes */}
          <Route path="/login" element={<LoginPage />} />
          <Route path="/signup" element={<SignupPage />} />
          <Route path="/forgot-password" element={<ForgotPassword />} />
          <Route path="/reset-password" element={<ResetPassword />} />
          
          {/* Layout Routes with Persistent Sidebar */}
          <Route element={
            <ProtectedRoute>
              <AppLayout />
            </ProtectedRoute>
          }>
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/courses" element={<Courses />} />
            <Route path="/practice" element={<Practice />} />
            <Route path="/ved" element={<VedPage />} />
            <Route path="/student/mock-tests" element={<MockTestTaker />} />
            <Route path="/automated-mock-tests" element={<AutomatedMockTests />} />
          </Route>
          
          {/* Other Protected Routes */}
          <Route path="/assessment/start" element={
            <ProtectedRoute>
              <SubjectSelection />
            </ProtectedRoute>
          } />
          
          <Route path="/assessment/test/:sessionId" element={
            <ProtectedRoute>
              <AssessmentTest />
            </ProtectedRoute>
          } />
          
          <Route path="/assessment/results/:sessionId" element={
            <ProtectedRoute>
              <AssessmentResults />
            </ProtectedRoute>
          } />
          
          <Route path="/recommendations/:studentId" element={
            <ProtectedRoute>
              <Recommendations />
            </ProtectedRoute>
          } />
          
          {/* Progress Tracking Routes */}
          <Route path="/progress" element={
            <ProtectedRoute>
              <ProgressPage />
            </ProtectedRoute>
          } />
          
          {/* New Routes */}
          <Route path="/practice-old" element={
            <ProtectedRoute>
              <PracticePage />
            </ProtectedRoute>
          } />
          
          <Route path="/resources" element={
            <ProtectedRoute>
              <ResourcePage />
            </ProtectedRoute>
          } />
          
          
          {/* Admin Routes */}
          <Route path="/admin/login" element={<AdminLogin />} />
          <Route path="/admin/*" element={<AdminDashboard />} />
          
          {/* Default Route */}
          <Route path="/" element={<WelcomePage />} />
          <Route path="/home" element={<Home />} />
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
