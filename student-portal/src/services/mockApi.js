// Mock API service for development
// This will be replaced with real API calls when backend is connected

// Mock authentication
export const mockLogin = async (credentials) => {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 500));
  
  // Always succeed with any credentials
  const token = 'mock-jwt-token-' + Date.now();
  const username = credentials.email?.split('@')[0] || 'user';
  
  // Store user info in localStorage
  localStorage.setItem('token', token);
  localStorage.setItem('user', JSON.stringify({
    id: 1,
    username: username,
    full_name: 'Test Student',
    email: credentials.email || 'student@example.com'
  }));
  
  console.log('Login successful with:', credentials);
  return { success: true, token, user: { username } };
};

export const mockSignup = async (userData) => {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 1000));
  
  // Simple validation - accept any input
  if (userData.email && userData.password) {
    const token = 'mock-jwt-token-' + Date.now();
    const username = userData.email.split('@')[0];
    localStorage.setItem('token', token);
    localStorage.setItem('user', JSON.stringify({
      id: 1,
      username: username,
      full_name: userData.full_name || username,
      email: userData.email
    }));
    return { success: true, token, user: { username: username } };
  } else {
    throw new Error('Please provide email and password');
  }
};

export const mockLogout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('user');
};

export const getCurrentUser = () => {
  const user = localStorage.getItem('user');
  return user ? JSON.parse(user) : null;
};

export const isAuthenticated = () => {
  return !!localStorage.getItem('token');
};

// Mock data fetching functions
export const getSubjects = async () => {
  const response = await fetch('/mock/mockSubjects.json');
  return response.json();
};

export const getQuestions = async (sessionId) => {
  const response = await fetch('/mock/mockQuestions.json');
  return response.json();
};

export const getResults = async (sessionId) => {
  const response = await fetch('/mock/mockResults.json');
  return response.json();
};

export const getRecommendations = async () => {
  const response = await fetch('/mock/mockRecommendations.json');
  return response.json();
};

// Mock assessment submission
export const submitAssessment = async (sessionId, answers) => {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 2000));
  
  // Return mock results
  const response = await fetch('/mock/mockResults.json');
  return response.json();
};

// Mock assessment start
export const startAssessment = async (subjectIds, numQuestionsPerSubject = 10) => {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 1000));
  
  // Return mock questions
  const response = await fetch('/mock/mockQuestions.json');
  return response.json();
};

// Reset database (for development purposes)
export const resetDatabase = () => {
  localStorage.clear();
  console.log('Database reset successfully');
  return { success: true, message: 'Database reset successfully' };
};
