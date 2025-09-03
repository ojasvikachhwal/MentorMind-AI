# MentorMind Admin Panel

A comprehensive admin panel for managing students, assessments, courses, and viewing analytics in the MentorMind learning platform.

## Features

### 🔐 Authentication
- **Admin Login**: Secure login with JWT tokens
- **Default Credentials**: `admin` / `password123`
- **Route Protection**: All admin routes require authentication

### 👥 Student Management
- View all students with pagination
- Search students by name or email
- Delete students (with confirmation)
- View student details including assessment scores and assigned courses

### 📊 Assessment Management
- View all student assessment results
- Filter by subject (Operating Systems, Computer Networks, OOPs, DBMS, Coding)
- Filter by score range (Beginner: 0-40%, Intermediate: 40-70%, Advanced: 70-100%)
- Search by student name or email
- Pagination support

### 📚 Course Management
- View all available courses
- Add new courses with validation
- Edit existing courses
- Delete courses
- Course fields: Title, Subject, Level, URL, Description
- URL validation (must be http/https)

### 📈 Reports & Analytics
- **Average Scores by Subject**: Visual representation with progress bars
- **Course Popularity**: Number of students per course
- **Statistics Overview**: Total students, courses, and average scores
- **CSV Export**: Download reports for students, assessments, and courses

### 🎨 UI Features
- **Responsive Design**: Works on desktop and mobile
- **Dark Mode Toggle**: Switch between light and dark themes
- **Toast Notifications**: Success/error messages for all actions
- **Loading States**: Spinners and skeleton loaders
- **Empty States**: Friendly messages when no data is available

## Getting Started

### 1. Backend Setup
Ensure the FastAPI backend is running with admin endpoints:

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Initialize Admin User
Run the admin initialization script:

```bash
cd backend
python init_admin_simple.py
```

This creates the default admin user: `admin` / `password123`

### 3. Frontend Setup
Install dependencies and start the React app:

```bash
cd student-portal
npm install
npm run dev
```

### 4. Access Admin Panel
Navigate to `/admin/login` and use the default credentials.

## API Endpoints

### Authentication
- `POST /api/admin/login` - Admin login

### Students
- `GET /api/admin/students` - List all students
- `DELETE /api/admin/students/{id}` - Delete student

### Assessments
- `GET /api/admin/assessments` - List all assessments (with filters)

### Courses
- `GET /api/admin/courses` - List all courses
- `POST /api/admin/courses` - Create new course
- `PUT /api/admin/courses/{id}` - Update course
- `DELETE /api/admin/courses/{id}` - Delete course

### Reports
- `GET /api/admin/reports/average-scores` - Subject-wise average scores
- `GET /api/admin/reports/course-popularity` - Course popularity data
- `POST /api/admin/reports/export-csv` - Export data to CSV

## Component Structure

```
src/pages/admin/
├── AdminLogin.jsx          # Login form
├── AdminDashboard.jsx      # Main dashboard layout with routing
├── Students.jsx            # Student management
├── Assessments.jsx         # Assessment management
├── Courses.jsx             # Course management
└── Reports.jsx             # Analytics and reports
```

## State Management

Each component manages its own state using React hooks:
- `useState` for local component state
- `useEffect` for API calls and side effects
- Toast notifications for user feedback
- Loading states for better UX

## Styling

- **Tailwind CSS**: Utility-first CSS framework
- **Heroicons**: Beautiful SVG icons
- **Responsive Design**: Mobile-first approach
- **Dark Mode**: CSS-based theme switching

## Security Features

- JWT token authentication
- Protected admin routes
- Input validation and sanitization
- CSRF protection through proper headers
- Secure password handling

## Future Enhancements

- **Real-time Updates**: WebSocket integration for live data
- **Advanced Analytics**: Interactive charts with Chart.js or Recharts
- **Bulk Operations**: Import/export multiple students/courses
- **Audit Logs**: Track all admin actions
- **Role-based Access**: Multiple admin levels with different permissions
- **Email Notifications**: Automated alerts for important events

## Troubleshooting

### Common Issues

1. **Authentication Failed**
   - Check if admin user exists in database
   - Verify JWT token in localStorage
   - Ensure backend is running

2. **API Errors**
   - Check browser console for error details
   - Verify API endpoints are accessible
   - Check CORS configuration

3. **Database Issues**
   - Ensure database is running and accessible
   - Check database schema matches models
   - Verify admin table exists

### Development Tips

- Use browser dev tools to inspect network requests
- Check React DevTools for component state
- Monitor console for JavaScript errors
- Test responsive design on different screen sizes

## Contributing

When adding new features to the admin panel:

1. Follow the existing component structure
2. Use consistent naming conventions
3. Add proper error handling
4. Include loading states
5. Test on different devices
6. Update this documentation

## License

This project is part of the MentorMind learning platform.
