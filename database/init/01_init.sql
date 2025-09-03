-- Initialize MentorMind Database
-- This script creates sample data for testing

-- Insert sample badges
INSERT INTO badges (name, description, icon_url, category, criteria, points_value, is_active, created_at) VALUES
('First Steps', 'Complete your first quiz', '/icons/first-steps.png', 'achievement', '{"total_quizzes": 1}', 10, true, NOW()),
('Quick Learner', 'Complete 5 quizzes', '/icons/quick-learner.png', 'achievement', '{"total_quizzes": 5}', 25, true, NOW()),
('Streak Master', 'Maintain a 7-day learning streak', '/icons/streak-master.png', 'milestone', '{"streak_days": 7}', 50, true, NOW()),
('Perfect Score', 'Get 100% on any quiz', '/icons/perfect-score.png', 'achievement', '{"accuracy_rate": 1.0}', 30, true, NOW()),
('Topic Explorer', 'Complete quizzes in 3 different topics', '/icons/topic-explorer.png', 'achievement', '{"topics_covered": 3}', 40, true, NOW())
ON CONFLICT (name) DO NOTHING;

-- Insert sample quizzes
INSERT INTO quizzes (title, description, topic, difficulty_level, time_limit, is_active, created_at, updated_at) VALUES
('Database Fundamentals', 'Test your knowledge of basic database concepts', 'database', 'easy', 15, true, NOW(), NOW()),
('SQL Basics', 'Learn and practice SQL queries', 'database', 'medium', 20, true, NOW(), NOW()),
('Algorithm Basics', 'Introduction to algorithms and complexity', 'algorithms', 'easy', 15, true, NOW(), NOW()),
('Network Fundamentals', 'Basic computer network concepts', 'networks', 'easy', 15, true, NOW(), NOW()),
('OOP Concepts', 'Object-oriented programming fundamentals', 'oop', 'easy', 15, true, NOW(), NOW())
ON CONFLICT DO NOTHING;

-- Insert sample questions for Database Fundamentals quiz
INSERT INTO questions (quiz_id, question_text, question_type, options, correct_answer, explanation, difficulty_score, topic_tags, created_at) VALUES
(1, 'What does SQL stand for?', 'mcq', '["Structured Query Language", "Simple Query Language", "Standard Query Language", "System Query Language"]', 'Structured Query Language', 'SQL stands for Structured Query Language, which is the standard language for relational database management systems.', 1.0, '["sql", "database"]', NOW()),
(1, 'Which of the following is NOT a type of database?', 'mcq', '["Relational", "NoSQL", "Object-oriented", "Linear"]', 'Linear', 'Linear is not a database type. Common database types include relational, NoSQL, object-oriented, and hierarchical databases.', 2.0, '["database_types"]', NOW()),
(1, 'What is a primary key?', 'mcq', '["A key that opens the database", "A unique identifier for each record", "A backup key", "A security key"]', 'A unique identifier for each record', 'A primary key is a unique identifier for each record in a database table. It ensures data integrity and allows for efficient data retrieval.', 2.5, '["primary_key", "database_design"]', NOW())
ON CONFLICT DO NOTHING;

-- Insert sample questions for Algorithm Basics quiz
INSERT INTO questions (quiz_id, question_text, question_type, options, correct_answer, explanation, difficulty_score, topic_tags, created_at) VALUES
(3, 'What is the time complexity of linear search?', 'mcq', '["O(1)", "O(log n)", "O(n)", "O(n²)"]', 'O(n)', 'Linear search has O(n) time complexity because it may need to check every element in the worst case scenario.', 2.0, '["algorithms", "complexity", "searching"]', NOW()),
(3, 'What is the space complexity of quicksort?', 'mcq', '["O(1)", "O(log n)", "O(n)", "O(n²)"]', 'O(log n)', 'Quicksort has O(log n) space complexity due to the recursive call stack, though it can be optimized to O(1) with tail recursion optimization.', 3.0, '["algorithms", "complexity", "sorting"]', NOW()),
(3, 'Which sorting algorithm has the best average-case time complexity?', 'mcq', '["Bubble Sort", "Insertion Sort", "Quick Sort", "Selection Sort"]', 'Quick Sort', 'Quick Sort has the best average-case time complexity of O(n log n) among the given options.', 2.5, '["algorithms", "sorting", "complexity"]', NOW())
ON CONFLICT DO NOTHING;

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_questions_quiz_id ON questions(quiz_id);
CREATE INDEX IF NOT EXISTS idx_quiz_attempts_user_id ON quiz_attempts(user_id);
CREATE INDEX IF NOT EXISTS idx_user_badges_user_id ON user_badges(user_id);

COMMIT;
