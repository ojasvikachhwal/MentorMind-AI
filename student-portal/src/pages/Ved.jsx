import React, { useState, useRef, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Send, Bot, User } from 'lucide-react';
import ProfileDropdown from '../components/ProfileDropdown';

const Ved = () => {
  const [messages, setMessages] = useState([
    { 
      role: "assistant", 
      content: "👋 Hi! I'm VED, your AI coding assistant. I can help you with programming concepts, code reviews, debugging, and learning new technologies. How can I assist you today?",
      timestamp: new Date()
    }
  ]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const chatEndRef = useRef(null);
  const inputRef = useRef(null);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  useEffect(() => {
    // Focus input on component mount
    if (inputRef.current) {
      inputRef.current.focus();
    }
  }, []);

  const sendMessage = async () => {
    if (!input.trim() || isTyping) return;
    
    const userMessage = { 
      role: 'user', 
      content: input.trim(),
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsTyping(true);

    try {
      // Call the VED chat API endpoint
      const response = await fetch('/api/v1/ved/ved-chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          messages: [...messages, userMessage],
          question: input.trim()
        }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: data.reply || data.message || 'Sorry, I encountered an error processing your request.',
        timestamp: new Date()
      }]);
    } catch (error) {
      console.error('VED Chat Error:', error);
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: '⚠️ Sorry, I\'m having trouble connecting right now. Please try again in a moment.',
        timestamp: new Date()
      }]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const formatTime = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString([], { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  return (
    <div className="ved-page">
      {/* Chat Area */}
      <div className="chat-container">
        <div className="chat-messages">
          {messages.map((message, index) => (
            <motion.div
              key={index}
              className={`message-container ${message.role === 'user' ? 'user-message' : 'ved-message'}`}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
            >
              <div className="message-content">
                <div className="message-header">
                  <div className="message-avatar">
                    {message.role === 'user' ? <User size={16} /> : <Bot size={16} />}
                  </div>
                  <span className="message-role">
                    {message.role === 'user' ? 'You' : 'VED'}
                  </span>
                  <span className="message-time">
                    {formatTime(message.timestamp)}
                  </span>
                </div>
                <div className="message-text">
                  {message.content}
                </div>
              </div>
            </motion.div>
          ))}

          {/* Typing Animation */}
          {isTyping && (
            <motion.div
              className="typing-container"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
            >
              <div className="typing-content">
                <div className="typing-avatar">
                  <Bot size={16} />
                </div>
                <div className="typing-text">
                  VED is typing
                  <span className="typing-dots">
                    <span className="dot">.</span>
                    <span className="dot">.</span>
                    <span className="dot">.</span>
                  </span>
                </div>
              </div>
            </motion.div>
          )}
          <div ref={chatEndRef} />
        </div>

        {/* Input Area */}
        <div className="input-container">
          <div className="input-wrapper">
            <textarea
              ref={inputRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask VED anything about coding, programming concepts, or get help with your code..."
              className="message-input"
              rows={1}
              disabled={isTyping}
            />
            <motion.button
              onClick={sendMessage}
              disabled={!input.trim() || isTyping}
              className="send-button"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <Send size={20} />
            </motion.button>
          </div>
        </div>
      </div>

      <style jsx>{`
        .ved-page {
          display: flex;
          flex-direction: column;
          height: 100vh;
          background-color: #F9FAFB;
          font-family: 'Inter', sans-serif;
        }

        .chat-container {
          flex: 1;
          display: flex;
          flex-direction: column;
          overflow: hidden;
        }

        .chat-messages {
          flex: 1;
          overflow-y: auto;
          padding: 1rem 2rem;
          display: flex;
          flex-direction: column;
          gap: 1rem;
        }

        .message-container {
          display: flex;
          margin-bottom: 0.5rem;
        }

        .user-message {
          justify-content: flex-end;
        }

        .ved-message {
          justify-content: flex-start;
        }

        .message-content {
          max-width: 75%;
          min-width: 200px;
        }

        .message-header {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          margin-bottom: 0.5rem;
          font-size: 0.875rem;
        }

        .message-avatar {
          width: 24px;
          height: 24px;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          color: white;
        }

        .user-message .message-avatar {
          background: linear-gradient(135deg, #7B2FF7, #F107A3);
        }

        .ved-message .message-avatar {
          background: linear-gradient(135deg, #3b82f6, #9333ea);
        }

        .message-role {
          font-weight: 600;
          color: #374151;
        }

        .message-time {
          color: #9CA3AF;
          font-size: 0.75rem;
        }

        .message-text {
          padding: 0.75rem 1rem;
          border-radius: 1rem;
          line-height: 1.6;
          white-space: pre-wrap;
          word-wrap: break-word;
        }

        .user-message .message-text {
          background: linear-gradient(135deg, #7B2FF7, #F107A3);
          color: white;
          border-bottom-right-radius: 0.25rem;
        }

        .ved-message .message-text {
          background: #E5E7EB;
          color: #374151;
          border-bottom-left-radius: 0.25rem;
        }

        .typing-container {
          display: flex;
          justify-content: flex-start;
          margin-bottom: 0.5rem;
        }

        .typing-content {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          padding: 0.75rem 1rem;
          background: #E5E7EB;
          border-radius: 1rem;
          border-bottom-left-radius: 0.25rem;
          max-width: 200px;
        }

        .typing-avatar {
          width: 24px;
          height: 24px;
          border-radius: 50%;
          background: linear-gradient(135deg, #3b82f6, #9333ea);
          display: flex;
          align-items: center;
          justify-content: center;
          color: white;
        }

        .typing-text {
          color: #6B7280;
          font-style: italic;
        }

        .typing-dots {
          display: inline-block;
        }

        .dot {
          animation: typing 1.4s infinite;
        }

        .dot:nth-child(2) {
          animation-delay: 0.2s;
        }

        .dot:nth-child(3) {
          animation-delay: 0.4s;
        }

        @keyframes typing {
          0%, 60%, 100% {
            opacity: 0;
          }
          30% {
            opacity: 1;
          }
        }

        .input-container {
          background: white;
          border-top: 1px solid #E5E7EB;
          padding: 1rem 2rem;
          position: sticky;
          bottom: 0;
        }

        .input-wrapper {
          display: flex;
          align-items: flex-end;
          gap: 0.75rem;
          max-width: 800px;
          margin: 0 auto;
        }

        .message-input {
          flex: 1;
          border: 1px solid #D1D5DB;
          border-radius: 1.5rem;
          padding: 0.75rem 1rem;
          font-size: 0.875rem;
          line-height: 1.5;
          resize: none;
          outline: none;
          transition: border-color 0.2s;
          font-family: inherit;
          min-height: 44px;
          max-height: 120px;
        }

        .message-input:focus {
          border-color: #7B2FF7;
          box-shadow: 0 0 0 3px rgba(123, 47, 247, 0.1);
        }

        .message-input:disabled {
          background-color: #F3F4F6;
          cursor: not-allowed;
        }

        .send-button {
          width: 44px;
          height: 44px;
          border-radius: 50%;
          background: linear-gradient(135deg, #7B2FF7, #F107A3);
          border: none;
          color: white;
          display: flex;
          align-items: center;
          justify-content: center;
          cursor: pointer;
          transition: all 0.2s ease;
          flex-shrink: 0;
        }

        .send-button:hover:not(:disabled) {
          transform: scale(1.05);
          box-shadow: 0 4px 12px rgba(123, 47, 247, 0.3);
        }

        .send-button:disabled {
          opacity: 0.5;
          cursor: not-allowed;
          transform: none;
        }

        /* Responsive Design */
        @media (max-width: 768px) {
          .header {
            padding: 1rem;
          }

          .header-title {
            font-size: 1.25rem;
          }

          .chat-messages {
            padding: 1rem;
          }

          .input-container {
            padding: 1rem;
          }

          .message-content {
            max-width: 85%;
          }
        }

        @media (max-width: 480px) {
          .header-left {
            gap: 0.5rem;
          }

          .header-icon {
            width: 24px;
            height: 24px;
          }

          .header-title {
            font-size: 1.125rem;
          }

          .message-content {
            max-width: 90%;
            min-width: 150px;
          }

          .message-text {
            padding: 0.5rem 0.75rem;
            font-size: 0.875rem;
          }
        }
      `}</style>
    </div>
  );
};

export default Ved;
