import { useNavigate } from 'react-router-dom';
import { Button } from '../../components/ui/Button';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '../../components/ui/Card';
import { getCurrentUser, logout } from '../../services/api';
import { BookOpen, BarChart3, GraduationCap, LogOut, User, TrendingUp, MessageSquare, Code } from 'lucide-react';

export default function Dashboard() {
  const navigate = useNavigate();
  const user = getCurrentUser();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const dashboardCards = [
    {
      title: 'Start New Assessment',
      description: 'Take a skill assessment to get personalized course recommendations',
      icon: BookOpen,
      action: () => navigate('/assessment/start'),
      color: 'bg-blue-500'
    },
    {
      title: 'View Past Results',
      description: 'Review your previous assessment results and progress',
      icon: BarChart3,
      action: () => navigate('/assessment/results/1'),
      color: 'bg-green-500'
    },
    {
      title: 'Recommended Courses',
      description: 'Browse courses tailored to your skill level and interests',
      icon: GraduationCap,
      action: () => navigate('/courses/recommendations'),
      color: 'bg-purple-500'
    },
    {
      title: 'Progress Dashboard',
      description: 'Track your learning progress with detailed analytics and insights',
      icon: TrendingUp,
      action: () => navigate('/progress'),
      color: 'bg-orange-500'
    },
    {
      title: 'AI Feedback',
      description: 'View personalized AI-generated feedback and recommendations',
      icon: MessageSquare,
      action: () => navigate('/progress/feedback'),
      color: 'bg-indigo-500'
    },
    {
      title: 'Coding Practice',
      description: 'Track your coding practice attempts and improvement',
      icon: Code,
      action: () => navigate('/progress/coding'),
      color: 'bg-teal-500'
    }
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-semibold text-gray-900">
                Student Learning Portal
              </h1>
            </div>
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <User className="h-5 w-5 text-gray-400" />
                <span className="text-sm text-gray-700">
                  Welcome, {user?.full_name || user?.username || 'Student'}
                </span>
              </div>
              <Button
                variant="outline"
                size="sm"
                onClick={handleLogout}
                className="flex items-center space-x-2"
              >
                <LogOut className="h-4 w-4" />
                <span>Logout</span>
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          {/* Welcome Section */}
          <div className="mb-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-2">
              Welcome back, {user?.full_name || user?.username || 'Student'}!
            </h2>
            <p className="text-gray-600">
              Ready to continue your learning journey? Choose an option below to get started.
            </p>
          </div>

          {/* Dashboard Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-3 gap-6">
            {dashboardCards.map((card, index) => (
              <Card key={index} className="hover:shadow-lg transition-shadow cursor-pointer">
                <CardHeader>
                  <div className="flex items-center space-x-3">
                    <div className={`p-2 rounded-lg ${card.color}`}>
                      <card.icon className="h-6 w-6 text-white" />
                    </div>
                    <CardTitle className="text-lg">{card.title}</CardTitle>
                  </div>
                  <CardDescription>{card.description}</CardDescription>
                </CardHeader>
                <CardContent>
                  <Button
                    onClick={card.action}
                    className="w-full"
                    size="lg"
                  >
                    Get Started
                  </Button>
                </CardContent>
              </Card>
            ))}
          </div>

          {/* Quick Stats */}
          <div className="mt-8">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Your Learning Stats</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <Card>
                <CardContent className="p-6">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-blue-600">3</div>
                    <div className="text-sm text-gray-600">Assessments Completed</div>
                  </div>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="p-6">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-green-600">15</div>
                    <div className="text-sm text-gray-600">Courses Recommended</div>
                  </div>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="p-6">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-purple-600">75%</div>
                    <div className="text-sm text-gray-600">Average Score</div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
