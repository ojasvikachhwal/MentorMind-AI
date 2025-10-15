import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/v1/code';

const codeExecutionService = {
  /**
   * Execute code in real-time
   */
  async runCode(code, language, inputData = null) {
    try {
      const response = await axios.post(`${API_BASE_URL}/run-code`, {
        code,
        language,
        input_data: inputData
      }, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
          'Content-Type': 'application/json'
        }
      });
      return response.data;
    } catch (error) {
      console.error('Code execution error:', error);
      throw new Error(error.response?.data?.detail || 'Failed to execute code');
    }
  },

  /**
   * Get AI feedback on code using Gemini
   */
  async getGeminiFeedback(code, language, output = null, error = null, question = null) {
    try {
      const response = await axios.post(`${API_BASE_URL}/gemini-feedback`, {
        code,
        language,
        output,
        error,
        question
      }, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
          'Content-Type': 'application/json'
        }
      });
      return response.data;
    } catch (error) {
      console.error('Gemini feedback error:', error);
      throw new Error(error.response?.data?.detail || 'Failed to get AI feedback');
    }
  },

  /**
   * Chat with VED AI assistant
   */
  async chatWithVED(code, language, question, context = null) {
    try {
      const response = await axios.post(`${API_BASE_URL}/ved-chat`, {
        code,
        language,
        question,
        context
      }, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
          'Content-Type': 'application/json'
        }
      });
      return response.data;
    } catch (error) {
      console.error('VED chat error:', error);
      throw new Error(error.response?.data?.detail || 'Failed to chat with VED');
    }
  },

  /**
   * Get supported programming languages
   */
  async getSupportedLanguages() {
    try {
      const response = await axios.get(`${API_BASE_URL}/supported-languages`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      return response.data;
    } catch (error) {
      console.error('Failed to get supported languages:', error);
      // Return fallback languages
      return {
        languages: [
          { value: 'python', label: 'Python', extension: '.py', description: 'General-purpose programming language' },
          { value: 'java', label: 'Java', extension: '.java', description: 'Object-oriented programming language' },
          { value: 'cpp', label: 'C++', extension: '.cpp', description: 'High-performance systems programming' },
          { value: 'javascript', label: 'JavaScript', extension: '.js', description: 'Web development and scripting' }
        ]
      };
    }
  }
};

export default codeExecutionService;
