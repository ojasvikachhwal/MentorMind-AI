import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../../components/ui/Button';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '../../components/ui/Card';
import { getSubjects, startAssessment } from '../../services/api';
import { Check, ArrowRight } from 'lucide-react';

export default function SubjectSelection() {
  const [subjects, setSubjects] = useState([]);
  const [selectedSubjects, setSelectedSubjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [starting, setStarting] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    loadSubjects();
  }, []);

  const loadSubjects = async () => {
    try {
      const subjectsData = await getSubjects();
      setSubjects(subjectsData);
    } catch (err) {
      setError('Failed to load subjects');
    } finally {
      setLoading(false);
    }
  };

  const toggleSubject = (subjectId) => {
    setSelectedSubjects(prev => 
      prev.includes(subjectId)
        ? prev.filter(id => id !== subjectId)
        : [...prev, subjectId]
    );
  };

  const selectAll = () => {
    setSelectedSubjects(subjects.map(subject => subject.id));
  };

  const deselectAll = () => {
    setSelectedSubjects([]);
  };

  const handleStartAssessment = async () => {
    if (selectedSubjects.length === 0) {
      setError('Please select at least one subject');
      return;
    }

    setStarting(true);
    setError('');

    try {
      const result = await startAssessment(selectedSubjects, 10);
      navigate(`/assessment/test/${result.session_id}`, { 
        state: { questions: result.questions, sessionId: result.session_id }
      });
    } catch (err) {
      setError('Failed to start assessment');
    } finally {
      setStarting(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading subjects...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Choose Your Subjects
          </h1>
          <p className="text-gray-600">
            Select the subjects you'd like to be assessed on. You can choose multiple subjects or all of them.
          </p>
        </div>

        {error && (
          <div className="mb-6 bg-destructive/10 border border-destructive/20 text-destructive px-4 py-3 rounded-md">
            {error}
          </div>
        )}

        <Card>
          <CardHeader>
            <div className="flex justify-between items-center">
              <div>
                <CardTitle>Available Subjects</CardTitle>
                <CardDescription>
                  Select the subjects you want to be assessed on
                </CardDescription>
              </div>
              <div className="flex space-x-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={selectAll}
                >
                  Select All
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={deselectAll}
                >
                  Deselect All
                </Button>
              </div>
            </div>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {subjects.map((subject) => (
                <div
                  key={subject.id}
                  className={`p-4 border rounded-lg cursor-pointer transition-all ${
                    selectedSubjects.includes(subject.id)
                      ? 'border-primary bg-primary/5'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                  onClick={() => toggleSubject(subject.id)}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex-1">
                      <h3 className="font-medium text-gray-900">{subject.name}</h3>
                      <p className="text-sm text-gray-600 mt-1">{subject.description}</p>
                    </div>
                    <div className="ml-4">
                      {selectedSubjects.includes(subject.id) ? (
                        <div className="w-6 h-6 bg-primary rounded-full flex items-center justify-center">
                          <Check className="w-4 h-4 text-white" />
                        </div>
                      ) : (
                        <div className="w-6 h-6 border-2 border-gray-300 rounded-full"></div>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>

            <div className="mt-6 pt-6 border-t">
              <div className="flex justify-between items-center">
                <div>
                  <p className="text-sm text-gray-600">
                    Selected: <span className="font-medium">{selectedSubjects.length}</span> subjects
                  </p>
                  <p className="text-xs text-gray-500 mt-1">
                    Each subject will have 10 questions with varying difficulty levels
                  </p>
                </div>
                <Button
                  onClick={handleStartAssessment}
                  disabled={selectedSubjects.length === 0 || starting}
                  className="flex items-center space-x-2"
                  size="lg"
                >
                  {starting ? (
                    <>
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                      <span>Starting...</span>
                    </>
                  ) : (
                    <>
                      <span>Start Assessment</span>
                      <ArrowRight className="w-4 h-4" />
                    </>
                  )}
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
