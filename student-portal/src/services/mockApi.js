// Mock API service for development
// This will be replaced with real API calls when backend is connected

// Mock authentication
export const mockLogin = async (credentials) => {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 1000));
  
  // Simple validation
  if (credentials.username === 'student' && credentials.password === 'password') {
    const token = 'mock-jwt-token-' + Date.now();
    localStorage.setItem('token', token);
    localStorage.setItem('user', JSON.stringify({
      id: 1,
      username: credentials.username,
      full_name: 'Test Student',
      email: 'student@example.com'
    }));
    return { success: true, token, user: { username: credentials.username } };
  } else {
    throw new Error('Invalid credentials');
  }
};

export const mockSignup = async (userData) => {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 1000));
  
  // Simple validation
  if (userData.username && userData.password && userData.email) {
    const token = 'mock-jwt-token-' + Date.now();
    localStorage.setItem('token', token);
    localStorage.setItem('user', JSON.stringify({
      id: 1,
      username: userData.username,
      full_name: userData.full_name || userData.username,
      email: userData.email
    }));
    return { success: true, token, user: { username: userData.username } };
  } else {
    throw new Error('Please fill in all required fields');
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
