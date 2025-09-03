import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import ProtectedRoute from './components/ProtectedRoute';

// Auth Pages
import Login from './pages/auth/Login';
import Signup from './pages/auth/Signup';
import ForgotPassword from './pages/auth/ForgotPassword';
import ResetPassword from './pages/auth/ResetPassword';

// Dashboard
import Dashboard from './pages/dashboard/Dashboard';

// Assessment Pages
import SubjectSelection from './pages/assessment/SubjectSelection';
import AssessmentTest from './pages/assessment/AssessmentTest';
import AssessmentResults from './pages/assessment/AssessmentResults';

// Course Pages
import CourseRecommendations from './pages/courses/CourseRecommendations';
import Recommendations from './pages/Recommendations';

// Progress Tracking Pages
import ProgressDashboard from './pages/progress/ProgressDashboard';
import AIFeedback from './pages/progress/AIFeedback';
import CodingPractice from './pages/progress/CodingPractice';

// Admin Pages
import AdminLogin from './pages/admin/AdminLogin';
import AdminDashboard from './pages/admin/AdminDashboard';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          {/* Public Routes */}
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/forgot-password" element={<ForgotPassword />} />
          <Route path="/reset-password" element={<ResetPassword />} />
          
          {/* Protected Routes */}
          <Route path="/dashboard" element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          } />
          
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
          
          <Route path="/courses/recommendations" element={
            <ProtectedRoute>
              <CourseRecommendations />
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
              <ProgressDashboard />
            </ProtectedRoute>
          } />
          
          <Route path="/progress/feedback" element={
            <ProtectedRoute>
              <AIFeedback />
            </ProtectedRoute>
          } />
          
          <Route path="/progress/coding" element={
            <ProtectedRoute>
              <CodingPractice />
            </ProtectedRoute>
          } />
          
          {/* Admin Routes */}
          <Route path="/admin/login" element={<AdminLogin />} />
          <Route path="/admin/*" element={<AdminDashboard />} />
          
          {/* Default redirect */}
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
