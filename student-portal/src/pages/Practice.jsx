import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { 
  Home, Edit3, Package, Brain, Play, Send, 
  Code, Terminal, Lightbulb, MessageCircle, 
  Clock, CheckCircle, AlertCircle, RefreshCw,
  Download, Copy, Trash2, Save
} from 'lucide-react';
import ProfileDropdown from '../components/ProfileDropdown';
import ved from '../services/ved';
import codeExecutionService from '../services/codeExecution';
import AceEditor from 'react-ace';
import 'ace-builds/src-noconflict/mode-python';
import 'ace-builds/src-noconflict/mode-c_cpp';
import 'ace-builds/src-noconflict/mode-java';
import 'ace-builds/src-noconflict/mode-javascript';
import 'ace-builds/src-noconflict/theme-github';
import 'ace-builds/src-noconflict/theme-monokai';
import 'ace-builds/src-noconflict/theme-dracula';
import 'ace-builds/src-noconflict/ext-language_tools';

const Practice = () => {
  const navigate = useNavigate();
  const [selectedLanguage, setSelectedLanguage] = useState('python');
  const [code, setCode] = useState(`# Python code example
def hello_world():
    print("Hello, World!")
    return "Success"

if __name__ == "__main__":
    result = hello_world()
    print(f"Result: {result}")
`);
  const [inputData, setInputData] = useState('');
  const [isExecuting, setIsExecuting] = useState(false);
  const [isGettingFeedback, setIsGettingFeedback] = useState(false);
  const [isChatting, setIsChatting] = useState(false);
  const [executionResult, setExecutionResult] = useState(null);
  const [geminiFeedback, setGeminiFeedback] = useState(null);
  const [vedResponse, setVedResponse] = useState(null);
  const [question, setQuestion] = useState('');
  const [supportedLanguages, setSupportedLanguages] = useState([]);
  const [editorTheme, setEditorTheme] = useState('github');
  const [showOutput, setShowOutput] = useState(true);
  const [showFeedback, setShowFeedback] = useState(true);
  const [showVED, setShowVED] = useState(true);
  const [executionHistory, setExecutionHistory] = useState([]);
  const [savedCodes, setSavedCodes] = useState([]);
  const outputRef = useRef(null);
  const feedbackRef = useRef(null);
  const vedRef = useRef(null);

  const codingQuestions = [
    {
      title: 'Two Sum Problem',
      description: 'Find two numbers in an array that add up to a target value',
      difficulty: 'Easy',
      code: {
        python: `def two_sum(nums, target):
    # Your solution here
    pass

# Test case
nums = [2, 7, 11, 15]
target = 9
result = two_sum(nums, target)
print(f"Indices: {result}")`,
        java: `public class TwoSum {
    public int[] twoSum(int[] nums, int target) {
        // Your solution here
        return new int[0];
    }
    
    public static void main(String[] args) {
        TwoSum solution = new TwoSum();
        int[] nums = {2, 7, 11, 15};
        int target = 9;
        int[] result = solution.twoSum(nums, target);
        System.out.println("Indices: " + java.util.Arrays.toString(result));
    }
}`,
        cpp: `#include <iostream>
#include <vector>
using namespace std;

vector<int> twoSum(vector<int>& nums, int target) {
    // Your solution here
    return {};
}

int main() {
    vector<int> nums = {2, 7, 11, 15};
    int target = 9;
    vector<int> result = twoSum(nums, target);
    cout << "Indices: ";
    for(int i : result) cout << i << " ";
    return 0;
}`
      }
    },
    {
      title: 'Reverse Linked List',
      description: 'Reverse a singly linked list',
      difficulty: 'Medium',
      code: {
        python: `class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverse_list(head):
    # Your solution here
    pass

# Test case
# Create a simple linked list: 1 -> 2 -> 3 -> 4 -> 5
head = ListNode(1)
head.next = ListNode(2)
head.next.next = ListNode(3)
head.next.next.next = ListNode(4)
head.next.next.next.next = ListNode(5)

result = reverse_list(head)
print("Reversed list:")`,
        java: `class ListNode {
    int val;
    ListNode next;
    ListNode() {}
    ListNode(int val) { this.val = val; }
    ListNode(int val, ListNode next) { this.val = val; this.next = next; }
}

public class ReverseLinkedList {
    public ListNode reverseList(ListNode head) {
        // Your solution here
        return null;
    }
    
    public static void main(String[] args) {
        // Test case
        ListNode head = new ListNode(1);
        head.next = new ListNode(2);
        head.next.next = new ListNode(3);
        head.next.next.next = new ListNode(4);
        head.next.next.next.next = new ListNode(5);
        
        ReverseLinkedList solution = new ReverseLinkedList();
        ListNode result = solution.reverseList(head);
        System.out.println("Reversed list:");
    }
}`,
        cpp: `#include <iostream>
using namespace std;

struct ListNode {
    int val;
    ListNode *next;
    ListNode() : val(0), next(nullptr) {}
    ListNode(int x) : val(x), next(nullptr) {}
    ListNode(int x, ListNode *next) : val(x), next(next) {}
};

class Solution {
public:
    ListNode* reverseList(ListNode* head) {
        // Your solution here
        return nullptr;
    }
};

int main() {
    // Test case
    ListNode* head = new ListNode(1);
    head->next = new ListNode(2);
    head->next->next = new ListNode(3);
    head->next->next->next = new ListNode(4);
    head->next->next->next->next = new ListNode(5);
    
    Solution solution;
    ListNode* result = solution.reverseList(head);
    cout << "Reversed list:" << endl;
    return 0;
}`
      }
    },
    {
      title: 'Binary Tree Traversal',
      description: 'Implement inorder, preorder, and postorder tree traversals',
      difficulty: 'Medium',
      code: {
        python: `class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def inorder_traversal(root):
    # Your solution here
    pass

def preorder_traversal(root):
    # Your solution here
    pass

def postorder_traversal(root):
    # Your solution here
    pass

# Test case
# Create a binary tree: [1,2,3,4,5,6,7]
root = TreeNode(1)
root.left = TreeNode(2)
root.right = TreeNode(3)
root.left.left = TreeNode(4)
root.left.right = TreeNode(5)
root.right.left = TreeNode(6)
root.right.right = TreeNode(7)

print("Inorder:", inorder_traversal(root))
print("Preorder:", preorder_traversal(root))
print("Postorder:", postorder_traversal(root))`,
        java: `class TreeNode {
    int val;
    TreeNode left;
    TreeNode right;
    TreeNode() {}
    TreeNode(int val) { this.val = val; }
    TreeNode(int val, TreeNode left, TreeNode right) {
        this.val = val;
        this.left = left;
        this.right = right;
    }
}

import java.util.*;

public class TreeTraversal {
    public List<Integer> inorderTraversal(TreeNode root) {
        // Your solution here
        return new ArrayList<>();
    }
    
    public List<Integer> preorderTraversal(TreeNode root) {
        // Your solution here
        return new ArrayList<>();
    }
    
    public List<Integer> postorderTraversal(TreeNode root) {
        // Your solution here
        return new ArrayList<>();
    }
    
    public static void main(String[] args) {
        // Test case
        TreeNode root = new TreeNode(1);
        root.left = new TreeNode(2);
        root.right = new TreeNode(3);
        root.left.left = new TreeNode(4);
        root.left.right = new TreeNode(5);
        root.right.left = new TreeNode(6);
        root.right.right = new TreeNode(7);
        
        TreeTraversal solution = new TreeTraversal();
        System.out.println("Inorder: " + solution.inorderTraversal(root));
        System.out.println("Preorder: " + solution.preorderTraversal(root));
        System.out.println("Postorder: " + solution.postorderTraversal(root));
    }
}`,
        cpp: `#include <iostream>
#include <vector>
using namespace std;

struct TreeNode {
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode() : val(0), left(nullptr), right(nullptr) {}
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
    TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
};

class Solution {
public:
    vector<int> inorderTraversal(TreeNode* root) {
        // Your solution here
        return {};
    }
    
    vector<int> preorderTraversal(TreeNode* root) {
        // Your solution here
        return {};
    }
    
    vector<int> postorderTraversal(TreeNode* root) {
        // Your solution here
        return {};
    }
};

int main() {
    // Test case
    TreeNode* root = new TreeNode(1);
    root->left = new TreeNode(2);
    root->right = new TreeNode(3);
    root->left->left = new TreeNode(4);
    root->left->right = new TreeNode(5);
    root->right->left = new TreeNode(6);
    root->right->right = new TreeNode(7);
    
    Solution solution;
    vector<int> inorder = solution.inorderTraversal(root);
    vector<int> preorder = solution.preorderTraversal(root);
    vector<int> postorder = solution.postorderTraversal(root);
    
    cout << "Inorder: ";
    for(int val : inorder) cout << val << " ";
    cout << endl;
    
    return 0;
}`
      }
    }
  ];

  // Load supported languages on component mount
  useEffect(() => {
    loadSupportedLanguages();
    loadSavedCodes();
  }, []);

  const loadSupportedLanguages = async () => {
    try {
      const response = await codeExecutionService.getSupportedLanguages();
      setSupportedLanguages(response.languages);
    } catch (error) {
      console.error('Failed to load languages:', error);
      // Fallback to default languages
      setSupportedLanguages([
    { value: 'python', label: 'Python', mode: 'python' },
        { value: 'java', label: 'Java', mode: 'java' },
    { value: 'cpp', label: 'C++', mode: 'c_cpp' },
        { value: 'javascript', label: 'JavaScript', mode: 'javascript' }
      ]);
    }
  };

  const loadSavedCodes = () => {
    const saved = localStorage.getItem('savedCodes');
    if (saved) {
      setSavedCodes(JSON.parse(saved));
    }
  };

  const saveCode = () => {
    const newCode = {
      id: Date.now(),
      title: `Code ${savedCodes.length + 1}`,
      language: selectedLanguage,
      code: code,
      timestamp: new Date().toISOString()
    };
    const updatedCodes = [...savedCodes, newCode];
    setSavedCodes(updatedCodes);
    localStorage.setItem('savedCodes', JSON.stringify(updatedCodes));
  };

  const loadCode = (savedCode) => {
    setCode(savedCode.code);
    setSelectedLanguage(savedCode.language);
  };

  const getDefaultCode = (language) => {
    switch (language) {
      case 'python':
        return `# Python code example
def hello_world():
    print("Hello, World!")
    return "Success"

if __name__ == "__main__":
    result = hello_world()
    print(f"Result: {result}")
`;
      case 'cpp':
        return `#include <iostream>
using namespace std;

int main() {
    cout << "Hello World!" << endl;
    return 0;
}`;
      case 'java':
        return `public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}`;
      case 'javascript':
        return `// JavaScript code example
function helloWorld() {
    console.log("Hello, World!");
    return "Success";
}

// Test the function
const result = helloWorld();
console.log(\`Result: \${result}\`);`;
      default:
        return '';
    }
  };

  const handleRunCode = async () => {
    if (!code.trim()) {
      setExecutionResult({
        output: '',
        error: 'Please write some code first!',
        execution_time: 0,
        exit_code: 1
      });
      return;
    }

    setIsExecuting(true);
    setExecutionResult(null);

    try {
      const result = await codeExecutionService.runCode(code, selectedLanguage, inputData);
      setExecutionResult(result);
      
      // Add to execution history
      const historyItem = {
        id: Date.now(),
        language: selectedLanguage,
        code: code,
        result: result,
        timestamp: new Date().toISOString()
      };
      setExecutionHistory(prev => [historyItem, ...prev.slice(0, 9)]); // Keep last 10

      // Auto-scroll to output
      if (outputRef.current) {
        outputRef.current.scrollIntoView({ behavior: 'smooth' });
      }
    } catch (error) {
      setExecutionResult({
        output: '',
        error: error.message,
        execution_time: 0,
        exit_code: 1
      });
    } finally {
      setIsExecuting(false);
    }
  };

  const handleGetFeedback = async () => {
    if (!code.trim()) {
      setGeminiFeedback({
        feedback: 'Please write some code first!',
        suggestions: [],
        score: 0,
        optimizations: []
      });
      return;
    }

    setIsGettingFeedback(true);
    setGeminiFeedback(null);

    try {
      const result = await codeExecutionService.getGeminiFeedback(
        code, 
        selectedLanguage, 
        executionResult?.output, 
        executionResult?.error,
        question
      );
      setGeminiFeedback(result);

      // Auto-scroll to feedback
      if (feedbackRef.current) {
        feedbackRef.current.scrollIntoView({ behavior: 'smooth' });
      }
    } catch (error) {
      setGeminiFeedback({
        feedback: `Failed to get feedback: ${error.message}`,
        suggestions: ['Try running your code first', 'Check for syntax errors'],
        score: 0,
        optimizations: []
      });
    } finally {
      setIsGettingFeedback(false);
    }
  };

  const handleVEDChat = async () => {
    if (!question.trim()) {
      setVedResponse({
        reply: 'Please ask a question about your code!',
        suggestions: [],
        related_topics: []
      });
      return;
    }

    setIsChatting(true);
    setVedResponse(null);

    try {
      const result = await codeExecutionService.chatWithVED(
        code, 
        selectedLanguage, 
        question,
        executionResult ? `Output: ${executionResult.output}\nError: ${executionResult.error || 'None'}` : null
      );
      setVedResponse(result);

      // Auto-scroll to VED response
      if (vedRef.current) {
        vedRef.current.scrollIntoView({ behavior: 'smooth' });
      }
    } catch (error) {
      setVedResponse({
        reply: `Failed to get VED response: ${error.message}`,
        suggestions: ['Try asking a simpler question', 'Check your internet connection'],
        related_topics: []
      });
    } finally {
      setIsChatting(false);
    }
  };

  const handleQuestionSubmit = async () => {
    await handleVEDChat();
  };

  const handleLanguageChange = (newLanguage) => {
    setSelectedLanguage(newLanguage);
    setCode(getDefaultCode(newLanguage));
    setExecutionResult(null);
    setGeminiFeedback(null);
    setVedResponse(null);
  };

  const handleQuestionSelect = (question) => {
    if (question.code && question.code[selectedLanguage]) {
      setCode(question.code[selectedLanguage]);
    }
    setExecutionResult(null);
    setGeminiFeedback(null);
    setVedResponse(null);
  };

  const clearAll = () => {
    setCode('');
    setInputData('');
    setExecutionResult(null);
    setGeminiFeedback(null);
    setVedResponse(null);
    setQuestion('');
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
  };

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.ctrlKey && e.key === 'Enter') {
        e.preventDefault();
        handleRunCode();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [code, selectedLanguage, inputData]);

  const handleNavigation = (path) => {
    navigate(path);
  };

  return (
    <div className="practice-page">
      {/* Top Navigation Bar */}
      <div className="top-nav">
        <div className="nav-items">
          <button 
            className="nav-item"
            onClick={() => handleNavigation('/dashboard')}
          >
            <Home size={20} />
            Home
          </button>
          <button 
            className="nav-item active"
            onClick={() => handleNavigation('/practice')}
          >
            <Edit3 size={20} />
            Practice
          </button>
          <button 
            className="nav-item"
            onClick={() => handleNavigation('/courses')}
          >
            <Package size={20} />
            Resource
          </button>
          <button 
            className="nav-item"
            onClick={() => handleNavigation('/ved')}
          >
            <Brain size={20} />
            VED
          </button>
        </div>
        
        <ProfileDropdown />
      </div>

      <div className="practice-content">
        {/* Left Panel - Questions & Saved Codes */}
        <div className="left-panel">
          <div className="panel-header">
            <h2 className="panel-title">Coding Practice</h2>
          </div>
          
          {/* Coding Questions */}
          <div className="section">
            <h3 className="section-title">Practice Problems</h3>
          <div className="questions-list">
            {codingQuestions.map((question, index) => (
              <motion.button
                key={index}
                className="question-item"
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                  onClick={() => handleQuestionSelect(question)}
                >
                  <div className="question-header">
                    <span className="question-title">{question.title}</span>
                    <span className={`difficulty ${question.difficulty.toLowerCase()}`}>
                      {question.difficulty}
                    </span>
                  </div>
                  <p className="question-description">{question.description}</p>
              </motion.button>
            ))}
          </div>
        </div>

          {/* Saved Codes */}
          {savedCodes.length > 0 && (
            <div className="section">
              <h3 className="section-title">Saved Codes</h3>
              <div className="saved-codes-list">
                {savedCodes.map((savedCode) => (
                  <motion.button
                    key={savedCode.id}
                    className="saved-code-item"
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                    onClick={() => loadCode(savedCode)}
                  >
                    <div className="saved-code-header">
                      <span className="saved-code-title">{savedCode.title}</span>
                      <span className="saved-code-language">{savedCode.language}</span>
                    </div>
                    <span className="saved-code-time">
                      {new Date(savedCode.timestamp).toLocaleDateString()}
                    </span>
                  </motion.button>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Right Panel - Code Editor & Output */}
        <div className="right-panel">
          {/* Toolbar */}
          <div className="toolbar">
            <div className="toolbar-left">
          <div className="language-selector">
                <label htmlFor="language-select">Language:</label>
            <select
              id="language-select"
              value={selectedLanguage}
                  onChange={(e) => handleLanguageChange(e.target.value)}
              className="language-select"
            >
                  {supportedLanguages.map((lang) => (
                <option key={lang.value} value={lang.value}>
                  {lang.label}
                </option>
              ))}
            </select>
              </div>
              
              <div className="theme-selector">
                <label htmlFor="theme-select">Theme:</label>
                <select
                  id="theme-select"
                  value={editorTheme}
                  onChange={(e) => setEditorTheme(e.target.value)}
                  className="theme-select"
                >
                  <option value="github">GitHub</option>
                  <option value="monokai">Monokai</option>
                  <option value="dracula">Dracula</option>
                </select>
              </div>
            </div>
            
            <div className="toolbar-right">
              <motion.button
                className="toolbar-btn"
                onClick={saveCode}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                title="Save Code"
              >
                <Save size={16} />
              </motion.button>
              
              <motion.button
                className="toolbar-btn"
                onClick={() => copyToClipboard(code)}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                title="Copy Code"
              >
                <Copy size={16} />
              </motion.button>
              
              <motion.button
                className="toolbar-btn"
                onClick={clearAll}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                title="Clear All"
              >
                <Trash2 size={16} />
              </motion.button>
            </div>
          </div>

          {/* Code Editor */}
          <div className="code-editor-container">
            <AceEditor
              mode={supportedLanguages.find(lang => lang.value === selectedLanguage)?.mode || 'python'}
              theme={editorTheme}
              value={code}
              onChange={setCode}
              name="code-editor"
              editorProps={{ $blockScrolling: true }}
              width="100%"
              height="400px"
              fontSize={14}
              showPrintMargin={true}
              showGutter={true}
              highlightActiveLine={true}
              setOptions={{
                enableBasicAutocompletion: true,
                enableLiveAutocompletion: true,
                enableSnippets: true,
                showLineNumbers: true,
                tabSize: 2,
                wrap: true,
                autoScrollEditorIntoView: true
              }}
              style={{
                border: '1px solid #E5E7EB',
                borderRadius: '0.75rem',
                backgroundColor: '#F9FAFB'
              }}
            />
          </div>

          {/* Input Data */}
          <div className="input-section">
            <label htmlFor="input-data">Input Data (optional):</label>
            <textarea
              id="input-data"
              value={inputData}
              onChange={(e) => setInputData(e.target.value)}
              placeholder="Enter input data for your program..."
              className="input-textarea"
              rows={3}
            />
          </div>

          {/* Action Buttons */}
          <div className="action-buttons">
            <motion.button
              className="action-btn run-btn"
              onClick={handleRunCode}
              disabled={isExecuting}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <Play size={16} />
              {isExecuting ? 'Running...' : 'Run Code'}
              <span className="shortcut">Ctrl+Enter</span>
            </motion.button>
            
            <motion.button
              className="action-btn feedback-btn"
              onClick={handleGetFeedback}
              disabled={isGettingFeedback}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <Lightbulb size={16} />
              {isGettingFeedback ? 'Analyzing...' : 'Get AI Feedback'}
            </motion.button>
          </div>

          {/* Output Section */}
          <AnimatePresence>
            {showOutput && (
              <motion.div
                ref={outputRef}
                className="output-section"
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                exit={{ opacity: 0, height: 0 }}
              >
                <div className="section-header">
                  <h3 className="section-title">
                    <Terminal size={20} />
                    Execution Output
                  </h3>
                  <button
                    className="toggle-btn"
                    onClick={() => setShowOutput(!showOutput)}
                  >
                    {showOutput ? '−' : '+'}
                  </button>
                </div>
                
                <div className="output-content">
                  {executionResult ? (
                    <div className="execution-result">
                      {executionResult.output && (
                        <div className="output-success">
                          <CheckCircle size={16} className="success-icon" />
                          <pre>{executionResult.output}</pre>
                        </div>
                      )}
                      
                      {executionResult.error && (
                        <div className="output-error">
                          <AlertCircle size={16} className="error-icon" />
                          <pre>{executionResult.error}</pre>
                        </div>
                      )}
                      
                      <div className="execution-meta">
                        <span>Exit Code: {executionResult.exit_code}</span>
                        <span>Time: {executionResult.execution_time.toFixed(3)}s</span>
                      </div>
                    </div>
                  ) : (
                    <div className="output-placeholder">
                      Code output will appear here after execution...
                    </div>
                  )}
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Gemini Feedback Section */}
          <AnimatePresence>
            {showFeedback && (
              <motion.div
                ref={feedbackRef}
                className="feedback-section"
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                exit={{ opacity: 0, height: 0 }}
              >
                <div className="section-header">
                  <h3 className="section-title">
                    <Lightbulb size={20} />
                    AI Feedback
                  </h3>
                  <button
                    className="toggle-btn"
                    onClick={() => setShowFeedback(!showFeedback)}
                  >
                    {showFeedback ? '−' : '+'}
                  </button>
                </div>
                
                <div className="feedback-content">
                  {geminiFeedback ? (
                    <div className="feedback-result">
                      <div className="feedback-score">
                        Score: {geminiFeedback.score}/100
                      </div>
                      
                      <div className="feedback-text">
                        {geminiFeedback.feedback}
                      </div>
                      
                      {geminiFeedback.suggestions.length > 0 && (
                        <div className="feedback-suggestions">
                          <h4>Suggestions:</h4>
                          <ul>
                            {geminiFeedback.suggestions.map((suggestion, index) => (
                              <li key={index}>{suggestion}</li>
                            ))}
                          </ul>
                        </div>
                      )}
                      
                      {geminiFeedback.optimizations.length > 0 && (
                        <div className="feedback-optimizations">
                          <h4>Optimizations:</h4>
                          <ul>
                            {geminiFeedback.optimizations.map((optimization, index) => (
                              <li key={index}>{optimization}</li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </div>
                  ) : (
                    <div className="feedback-placeholder">
                      Click "Get AI Feedback" to analyze your code...
                    </div>
                  )}
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          {/* VED Chat Section */}
          <AnimatePresence>
            {showVED && (
              <motion.div
                ref={vedRef}
                className="ved-section"
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                exit={{ opacity: 0, height: 0 }}
              >
                <div className="section-header">
                  <h3 className="section-title">
                    <MessageCircle size={20} />
                    VED Assistant
                  </h3>
                  <button
                    className="toggle-btn"
                    onClick={() => setShowVED(!showVED)}
                  >
                    {showVED ? '−' : '+'}
                  </button>
                </div>
                
                <div className="ved-content">
                  <div className="ved-input">
            <input
              type="text"
                      placeholder="Ask VED a question about your code..."
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
                      className="ved-question-input"
                      onKeyPress={(e) => e.key === 'Enter' && handleVEDChat()}
            />
            <motion.button
                      className="ved-ask-btn"
                      onClick={handleVEDChat}
                      disabled={isChatting}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
                      <Send size={16} />
                      {isChatting ? 'Thinking...' : 'Ask'}
            </motion.button>
          </div>

                  {vedResponse && (
                    <div className="ved-response">
                      <div className="ved-reply">
                        {vedResponse.reply}
            </div>
                      
                      {vedResponse.suggestions.length > 0 && (
                        <div className="ved-suggestions">
                          <h4>Suggestions:</h4>
                          <ul>
                            {vedResponse.suggestions.map((suggestion, index) => (
                              <li key={index}>{suggestion}</li>
                            ))}
                          </ul>
          </div>
                      )}
                      
                      {vedResponse.related_topics.length > 0 && (
                        <div className="ved-topics">
                          <h4>Related Topics:</h4>
                          <div className="topic-tags">
                            {vedResponse.related_topics.map((topic, index) => (
                              <span key={index} className="topic-tag">{topic}</span>
                            ))}
            </div>
          </div>
                      )}
                    </div>
                  )}
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>

      <style jsx>{`
        .practice-page {
          min-height: 100vh;
          background-color: #f8fafc;
          font-family: 'Inter', sans-serif;
        }

        .top-nav {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 1rem 2rem;
          background: linear-gradient(135deg, #7B2FF7, #F107A3);
          color: white;
          box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }

        .nav-items {
          display: flex;
          gap: 1rem;
        }

        .nav-item {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          padding: 0.5rem 1rem;
          background: none;
          border: none;
          color: white;
          cursor: pointer;
          border-radius: 0.5rem;
          transition: all 0.2s ease;
          font-size: 0.875rem;
          font-weight: 500;
        }

        .nav-item:hover {
          background-color: rgba(255, 255, 255, 0.1);
        }

        .nav-item.active {
          background-color: rgba(255, 255, 255, 0.2);
          font-weight: 600;
        }

        .practice-content {
          display: flex;
          height: calc(100vh - 80px);
          gap: 1rem;
          padding: 1rem;
        }

        .left-panel {
          width: 350px;
          background: linear-gradient(180deg, #7B2FF7 0%, #F107A3 100%);
          color: white;
          padding: 1.5rem;
          border-radius: 1rem;
          overflow-y: auto;
          box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        .panel-header {
          margin-bottom: 2rem;
        }

        .panel-title {
          font-size: 1.5rem;
          font-weight: 600;
          margin: 0;
        }

        .section {
          margin-bottom: 2rem;
        }

        .section-title {
          font-size: 1rem;
          font-weight: 600;
          margin: 0 0 1rem 0;
          color: rgba(255, 255, 255, 0.9);
        }

        .questions-list {
          display: flex;
          flex-direction: column;
          gap: 0.75rem;
        }

        .question-item {
          padding: 1rem;
          background: rgba(255, 255, 255, 0.1);
          border: none;
          border-radius: 0.75rem;
          color: white;
          cursor: pointer;
          transition: all 0.2s ease;
          text-align: left;
          font-size: 0.875rem;
          line-height: 1.4;
        }

        .question-item:hover {
          background: rgba(255, 255, 255, 0.2);
          transform: translateX(5px);
        }

        .question-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 0.5rem;
        }

        .question-title {
          font-weight: 600;
          font-size: 0.9rem;
        }

        .difficulty {
          padding: 0.25rem 0.5rem;
          border-radius: 0.375rem;
          font-size: 0.75rem;
          font-weight: 500;
        }

        .difficulty.easy {
          background-color: rgba(34, 197, 94, 0.2);
          color: #22c55e;
        }

        .difficulty.medium {
          background-color: rgba(251, 191, 36, 0.2);
          color: #fbbf24;
        }

        .difficulty.hard {
          background-color: rgba(239, 68, 68, 0.2);
          color: #ef4444;
        }

        .question-description {
          margin: 0;
          font-size: 0.8rem;
          opacity: 0.8;
        }

        .saved-codes-list {
          display: flex;
          flex-direction: column;
          gap: 0.5rem;
        }

        .saved-code-item {
          padding: 0.75rem;
          background: rgba(255, 255, 255, 0.1);
          border: none;
          border-radius: 0.5rem;
          color: white;
          cursor: pointer;
          transition: all 0.2s ease;
          text-align: left;
          font-size: 0.8rem;
        }

        .saved-code-item:hover {
          background: rgba(255, 255, 255, 0.2);
        }

        .saved-code-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 0.25rem;
        }

        .saved-code-title {
          font-weight: 500;
        }

        .saved-code-language {
          font-size: 0.7rem;
          opacity: 0.8;
        }

        .saved-code-time {
          font-size: 0.7rem;
          opacity: 0.6;
        }

        .right-panel {
          flex: 1;
          background-color: #ffffff;
          border-radius: 1rem;
          padding: 1.5rem;
          overflow-y: auto;
          box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        .toolbar {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 1.5rem;
          padding: 1rem;
          background-color: #f8fafc;
          border-radius: 0.75rem;
          border: 1px solid #e2e8f0;
        }

        .toolbar-left {
          display: flex;
          gap: 1.5rem;
          align-items: center;
        }

        .toolbar-right {
          display: flex;
          gap: 0.5rem;
        }

        .language-selector,
        .theme-selector {
          display: flex;
          align-items: center;
          gap: 0.5rem;
        }

        .language-selector label,
        .theme-selector label {
          font-size: 0.875rem;
          font-weight: 500;
          color: #374151;
        }

        .language-select,
        .theme-select {
          padding: 0.5rem 0.75rem;
          border: 1px solid #d1d5db;
          border-radius: 0.5rem;
          background: white;
          font-size: 0.875rem;
          min-width: 120px;
        }

        .toolbar-btn {
          padding: 0.5rem;
          background: white;
          border: 1px solid #d1d5db;
          border-radius: 0.5rem;
          cursor: pointer;
          transition: all 0.2s ease;
          color: #374151;
        }

        .toolbar-btn:hover {
          background-color: #f3f4f6;
          border-color: #7B2FF7;
        }

        .code-editor-container {
          margin-bottom: 1.5rem;
          border: 1px solid #e2e8f0;
          border-radius: 0.75rem;
          overflow: hidden;
        }

        .input-section {
          margin-bottom: 1.5rem;
        }

        .input-section label {
          display: block;
          margin-bottom: 0.5rem;
          font-weight: 500;
          color: #374151;
        }

        .input-textarea {
          width: 100%;
          padding: 0.75rem;
          border: 1px solid #d1d5db;
          border-radius: 0.5rem;
          font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
          font-size: 0.875rem;
          resize: vertical;
          outline: none;
          transition: border-color 0.2s;
        }

        .input-textarea:focus {
          border-color: #7B2FF7;
        }

        .action-buttons {
          display: flex;
          gap: 1rem;
          margin-bottom: 1.5rem;
        }

        .action-btn {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          padding: 0.75rem 1.5rem;
          border: none;
          border-radius: 0.75rem;
          font-weight: 500;
          cursor: pointer;
          transition: all 0.2s ease;
          position: relative;
        }

        .run-btn {
          background: linear-gradient(135deg, #7B2FF7, #F107A3);
          color: white;
        }

        .feedback-btn {
          background: linear-gradient(135deg, #3b82f6, #9333ea);
          color: white;
        }

        .action-btn:hover:not(:disabled) {
          transform: scale(1.05);
          box-shadow: 0 4px 12px rgba(123, 47, 247, 0.3);
        }

        .action-btn:disabled {
          opacity: 0.6;
          cursor: not-allowed;
        }

        .shortcut {
          position: absolute;
          top: -0.5rem;
          right: -0.5rem;
          background: rgba(0, 0, 0, 0.1);
          padding: 0.25rem 0.5rem;
          border-radius: 0.25rem;
          font-size: 0.7rem;
          font-weight: 400;
        }

        .output-section,
        .feedback-section,
        .ved-section {
          margin-bottom: 1.5rem;
          border: 1px solid #e2e8f0;
          border-radius: 0.75rem;
          overflow: hidden;
        }

        .section-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 1rem 1.5rem;
          background-color: #f8fafc;
          border-bottom: 1px solid #e2e8f0;
        }

        .section-title {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          font-size: 1rem;
          font-weight: 600;
          color: #374151;
          margin: 0;
        }

        .toggle-btn {
          background: none;
          border: none;
          font-size: 1.25rem;
          cursor: pointer;
          color: #6b7280;
          padding: 0.25rem;
        }

        .output-content,
        .feedback-content,
        .ved-content {
          padding: 1.5rem;
        }

        .execution-result {
          font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
        }

        .output-success {
          display: flex;
          align-items: flex-start;
          gap: 0.5rem;
          margin-bottom: 1rem;
          padding: 1rem;
          background-color: #f0fdf4;
          border: 1px solid #bbf7d0;
          border-radius: 0.5rem;
        }

        .success-icon {
          color: #22c55e;
          flex-shrink: 0;
          margin-top: 0.125rem;
        }

        .output-error {
          display: flex;
          align-items: flex-start;
          gap: 0.5rem;
          margin-bottom: 1rem;
          padding: 1rem;
          background-color: #fef2f2;
          border: 1px solid #fecaca;
          border-radius: 0.5rem;
        }

        .error-icon {
          color: #ef4444;
          flex-shrink: 0;
          margin-top: 0.125rem;
        }

        .execution-meta {
          display: flex;
          gap: 1rem;
          font-size: 0.875rem;
          color: #6b7280;
        }

        .output-placeholder,
        .feedback-placeholder {
          text-align: center;
          color: #6b7280;
          font-style: italic;
          padding: 2rem;
        }

        .feedback-result {
          space-y: 1rem;
        }

        .feedback-score {
          display: inline-block;
          padding: 0.5rem 1rem;
          background: linear-gradient(135deg, #7B2FF7, #F107A3);
          color: white;
          border-radius: 0.5rem;
          font-weight: 600;
          margin-bottom: 1rem;
        }

        .feedback-text {
          margin-bottom: 1rem;
          line-height: 1.6;
        }

        .feedback-suggestions,
        .feedback-optimizations {
          margin-bottom: 1rem;
        }

        .feedback-suggestions h4,
        .feedback-optimizations h4 {
          font-size: 0.875rem;
          font-weight: 600;
          color: #374151;
          margin: 0 0 0.5rem 0;
        }

        .feedback-suggestions ul,
        .feedback-optimizations ul {
          margin: 0;
          padding-left: 1.5rem;
        }

        .feedback-suggestions li,
        .feedback-optimizations li {
          margin-bottom: 0.25rem;
          font-size: 0.875rem;
          color: #6b7280;
        }

        .ved-input {
          display: flex;
          gap: 0.5rem;
          margin-bottom: 1rem;
        }

        .ved-question-input {
          flex: 1;
          padding: 0.75rem;
          border: 1px solid #d1d5db;
          border-radius: 0.5rem;
          font-size: 0.875rem;
          outline: none;
          transition: border-color 0.2s;
        }

        .ved-question-input:focus {
          border-color: #7B2FF7;
        }

        .ved-ask-btn {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          padding: 0.75rem 1rem;
          background: linear-gradient(135deg, #7B2FF7, #F107A3);
          color: white;
          border: none;
          border-radius: 0.5rem;
          font-weight: 500;
          cursor: pointer;
          transition: all 0.2s ease;
        }

        .ved-ask-btn:hover:not(:disabled) {
          transform: scale(1.05);
        }

        .ved-ask-btn:disabled {
          opacity: 0.6;
          cursor: not-allowed;
        }

        .ved-response {
          space-y: 1rem;
        }

        .ved-reply {
          margin-bottom: 1rem;
          line-height: 1.6;
          padding: 1rem;
          background-color: #f8fafc;
          border-radius: 0.5rem;
        }

        .ved-suggestions h4,
        .ved-topics h4 {
          font-size: 0.875rem;
          font-weight: 600;
          color: #374151;
          margin: 0 0 0.5rem 0;
        }

        .ved-suggestions ul {
          margin: 0;
          padding-left: 1.5rem;
        }

        .ved-suggestions li {
          margin-bottom: 0.25rem;
          font-size: 0.875rem;
          color: #6b7280;
        }

        .topic-tags {
          display: flex;
          flex-wrap: wrap;
          gap: 0.5rem;
        }

        .topic-tag {
          padding: 0.25rem 0.75rem;
          background-color: #e0e7ff;
          color: #3730a3;
          border-radius: 1rem;
          font-size: 0.75rem;
          font-weight: 500;
        }

        /* Responsive Design */
        @media (max-width: 1024px) {
          .practice-content {
            flex-direction: column;
            height: auto;
          }

          .left-panel {
            width: 100%;
            max-height: 300px;
          }

          .right-panel {
            width: 100%;
          }
        }

        @media (max-width: 768px) {
          .top-nav {
            padding: 1rem;
          }

          .nav-items {
            gap: 0.5rem;
          }

          .nav-item {
            padding: 0.5rem;
            font-size: 0.75rem;
          }

          .practice-content {
            padding: 0.5rem;
          }

          .toolbar {
            flex-direction: column;
            gap: 1rem;
            align-items: stretch;
          }

          .toolbar-left {
            justify-content: center;
          }

          .action-buttons {
            flex-direction: column;
          }

          .ved-input {
            flex-direction: column;
          }
        }

        @media (max-width: 480px) {
          .top-nav {
            flex-direction: column;
            gap: 1rem;
          }

          .nav-items {
            flex-wrap: wrap;
            justify-content: center;
          }

          .toolbar-left {
            flex-direction: column;
            gap: 0.5rem;
          }
        }
      `}</style>
    </div>
  );
};

export default Practice;
