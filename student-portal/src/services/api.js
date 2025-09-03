import axios from 'axios';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Authentication functions
export const login = async (credentials) => {
  try {
    console.log('Attempting to login with:', credentials);
    
    // Try both endpoints - with and without the /api/v1 prefix
    let response;
    try {
      response = await api.post('/api/v1/auth/login', credentials);
    } catch (loginError) {
      console.log('First login attempt failed:', loginError);
      // Try alternative endpoint
      response = await api.post('/auth/login', credentials);
    }
    
    const { access_token, user } = response.data;
    console.log('Login successful:', user);
    
    localStorage.setItem('token', access_token);
    localStorage.setItem('user', JSON.stringify(user));
    
    return { success: true, token: access_token, user };
  } catch (error) {
    console.error('Login error:', error);
    throw new Error(error.response?.data?.detail || 'Login failed');
  }
};

export const signup = async (userData) => {
  try {
    // Validate email format
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(userData.email)) {
      throw new Error('Please enter a valid email address');
    }
    
    console.log('Attempting to register with:', userData);
    
    // Check if we're using the correct endpoint
    // Try both with and without the /api/v1 prefix
    let response;
    try {
      response = await api.post('/api/v1/auth/register', userData);
    } catch (registerError) {
      console.log('First registration attempt failed:', registerError);
      // Try alternative endpoint
      response = await api.post('/auth/register', userData);
    }
    
    const user = response.data;
    console.log('Registration successful:', user);
    
    // After successful signup, login the user
    const loginResponse = await login({
      username: userData.username,
      password: userData.password
    });
    
    return loginResponse;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Signup failed');
  }
};

export const logout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('user');
};

export const requestPasswordReset = async (data) => {
  try {
    const response = await api.post('/api/v1/auth/forgot-password', data);
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to request password reset');
  }
};

export const resetPassword = async (data) => {
  try {
    const response = await api.post('/api/v1/auth/reset-password', data);
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to reset password');
  }
};

export const getCurrentUser = () => {
  const user = localStorage.getItem('user');
  return user ? JSON.parse(user) : null;
};

export const isAuthenticated = () => {
  return !!localStorage.getItem('token');
};

// Assessment functions
export const getSubjects = async () => {
  try {
    const response = await api.get('/subjects');
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to fetch subjects');
  }
};

export const startAssessment = async (subjectIds, numQuestionsPerSubject = 10) => {
  try {
    const response = await api.post('/assessment/start', {
      subject_ids: subjectIds,
      num_questions_per_subject: numQuestionsPerSubject
    });
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to start assessment');
  }
};

export const submitAssessment = async (sessionId, answers) => {
  try {
    const response = await api.post(`/assessment/${sessionId}/submit`, {
      answers: answers
    });
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to submit assessment');
  }
};

export const getResults = async (sessionId) => {
  try {
    const response = await api.get(`/assessment/${sessionId}/results`);
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to fetch results');
  }
};

export const getLatestResults = async () => {
  try {
    const response = await api.get('/recommendations/latest');
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to fetch latest results');
  }
};

// Course recommendations
export const getRecommendations = async () => {
  try {
    const response = await api.get('/recommendations/latest');
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to fetch recommendations');
  }
};

export default api;
