import axios from 'axios';

const VED_API_URL = 'http://127.0.0.1:8000/api/v1/ved/ved-chat';

const ved = {
  async analyzeCode(code, question) {
    try {
      const userPrompt = question 
        ? `Code: ${code}\nQuestion: ${question}` 
        : `Please analyze this code: ${code}`;

      const response = await axios.post(VED_API_URL, {
        messages: [
          { role: 'user', content: userPrompt }
        ],
        question: userPrompt
      }, {
        headers: {
          'Content-Type': 'application/json'
        }
      });

      return response.data.reply;
    } catch (error) {
      console.error('VED analysis error:', error);
      return "I'm currently unable to help analyze that code. Please try again later.";
    }
  },

  async chat(messages, question) {
    try {
      const response = await axios.post(VED_API_URL, {
        messages: messages,
        question: question
      }, {
        headers: {
          'Content-Type': 'application/json'
        }
      });

      return response.data.reply;
    } catch (error) {
      console.error('VED chat error:', error);
      return "⚠️ Sorry, I'm having trouble connecting right now. Please try again in a moment.";
    }
  }
};

export default ved;
