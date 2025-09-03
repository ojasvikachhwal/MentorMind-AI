# Student Learning Portal

A modern React-based student learning platform with AI-powered assessment and course recommendations.

## Features

### 🔐 Authentication
- **Mock Authentication System**: Login/Signup with localStorage-based JWT tokens
- **Protected Routes**: Route protection with automatic redirects
- **Demo Credentials**: Username: `student`, Password: `password`

### 📊 Assessment System
- **Subject Selection**: Choose from multiple subjects (Data Structures, OOP, DBMS, OS, Web Development)
- **Interactive Quiz**: One question at a time with progress tracking
- **Difficulty Stratification**: Questions mixed by difficulty (easy, medium, hard)
- **Real-time Progress**: Visual progress bar and question navigation
- **Results Analysis**: Detailed breakdown with percentage scores and skill levels

### 🎯 Course Recommendations
- **Personalized Recommendations**: Based on assessment results
- **Skill Level Mapping**: Beginner, Intermediate, Advanced levels
- **Course Filtering**: Search and filter by subject, level, and keywords
- **Course Cards**: Rich course information with ratings and duration

### 📱 Modern UI/UX
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Tailwind CSS**: Modern styling with custom design system
- **shadcn/ui Components**: Professional UI components
- **Smooth Navigation**: Intuitive user flow and transitions

## Tech Stack

- **Frontend**: React 18 + Vite
- **Routing**: React Router DOM
- **Styling**: Tailwind CSS
- **UI Components**: shadcn/ui + Radix UI
- **Icons**: Lucide React
- **State Management**: React Hooks
- **HTTP Client**: Fetch API (ready for Axios integration)

## Project Structure

```
src/
├── components/
│   ├── ui/                 # Reusable UI components
│   │   ├── Button.jsx
│   │   ├── Input.jsx
│   │   ├── Card.jsx
│   │   └── Progress.jsx
│   └── ProtectedRoute.jsx  # Route protection component
├── pages/
│   ├── auth/              # Authentication pages
│   │   ├── Login.jsx
│   │   └── Signup.jsx
│   ├── dashboard/         # Main dashboard
│   │   └── Dashboard.jsx
│   ├── assessment/        # Assessment flow
│   │   ├── SubjectSelection.jsx
│   │   ├── AssessmentTest.jsx
│   │   └── AssessmentResults.jsx
│   └── courses/           # Course recommendations
│       └── CourseRecommendations.jsx
├── services/
│   └── mockApi.js         # Mock API service
├── lib/
│   └── utils.js           # Utility functions
├── App.jsx                # Main app component
└── main.jsx              # App entry point
```

## Getting Started

### Prerequisites
- Node.js (v16 or higher)
- npm or yarn

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd student-portal
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start the development server**
   ```bash
   npm run dev
   ```

4. **Open your browser**
   Navigate to `http://localhost:5173`

### Demo Login
- **Username**: `student`
- **Password**: `password`

## Usage Guide

### 1. Authentication
- Visit `/login` or `/signup`
- Use demo credentials or create a new account
- JWT token is stored in localStorage

### 2. Dashboard
- Main hub with quick access to all features
- View learning statistics
- Navigate to assessments or courses

### 3. Assessment Flow
1. **Subject Selection** (`/assessment/start`)
   - Choose subjects to be assessed on
   - Select all or specific subjects
   - Start assessment

2. **Take Assessment** (`/assessment/test/:id`)
   - Answer questions one by one
   - Navigate between questions
   - Submit when complete

3. **View Results** (`/assessment/results/:id`)
   - Detailed performance breakdown
   - Subject-wise analysis
   - Recommended courses

### 4. Course Recommendations
- Browse all available courses
- Filter by subject, level, or search terms
- View course details and enroll

## Mock Data

The application uses mock JSON files for development:

- **Subjects**: `/public/mock/mockSubjects.json`
- **Questions**: `/public/mock/mockQuestions.json`
- **Results**: `/public/mock/mockResults.json`
- **Courses**: `/public/mock/mockRecommendations.json`

## API Integration

The mock API service (`src/services/mockApi.js`) is designed to be easily replaced with real API calls:

```javascript
// Current mock implementation
export const getSubjects = async () => {
  const response = await fetch('/mock/mockSubjects.json');
  return response.json();
};

// Future real API implementation
export const getSubjects = async () => {
  const response = await axios.get('/api/subjects');
  return response.data;
};
```

## Customization

### Styling
- Modify `src/index.css` for global styles
- Update `tailwind.config.js` for theme customization
- Use CSS variables for consistent theming

### Components
- All UI components are in `src/components/ui/`
- Follow shadcn/ui patterns for consistency
- Use `cn()` utility for class merging

### Mock Data
- Update JSON files in `/public/mock/` for different test scenarios
- Modify `mockApi.js` for different API behaviors

## Development

### Available Scripts
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build

### Code Structure
- **Components**: Reusable UI elements
- **Pages**: Route-specific components
- **Services**: API and business logic
- **Utils**: Helper functions and utilities

## Future Enhancements

- [ ] Real API integration
- [ ] User profile management
- [ ] Course enrollment system
- [ ] Progress tracking
- [ ] Notifications
- [ ] Dark mode
- [ ] Internationalization
- [ ] PWA features

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For questions or issues, please open an issue in the repository.
