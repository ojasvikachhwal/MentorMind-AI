import React, { useEffect } from 'react';
import { 
  CheckCircle, 
  XCircle, 
  X 
} from 'lucide-react';

const Toast = ({ 
  type = 'success', 
  message, 
  isVisible, 
  onClose, 
  duration = 5000 
}) => {
  useEffect(() => {
    if (isVisible && duration > 0) {
      const timer = setTimeout(() => {
        onClose();
      }, duration);

      return () => clearTimeout(timer);
    }
  }, [isVisible, duration, onClose]);

  if (!isVisible) return null;

  const getToastStyles = () => {
    switch (type) {
      case 'success':
        return {
          bg: 'bg-green-50 dark:bg-green-900',
          border: 'border-green-200 dark:border-green-700',
          icon: 'text-green-400',
          text: 'text-green-800 dark:text-green-200',
          iconComponent: CheckCircle
        };
      case 'error':
        return {
          bg: 'bg-red-50 dark:bg-red-900',
          border: 'border-red-200 dark:border-red-700',
          icon: 'text-red-400',
          text: 'text-red-800 dark:text-red-200',
          iconComponent: XCircle
        };
      default:
        return {
          bg: 'bg-blue-50 dark:bg-blue-900',
          border: 'border-blue-200 dark:border-blue-700',
          icon: 'text-blue-400',
          text: 'text-blue-800 dark:text-blue-200',
          iconComponent: CheckCircle
        };
    }
  };

  const styles = getToastStyles();
  const IconComponent = styles.iconComponent;

  return (
    <div className="fixed top-4 right-4 z-50 max-w-sm w-full">
      <div className={`${styles.bg} ${styles.border} border rounded-lg shadow-lg p-4`}>
        <div className="flex items-start">
          <div className="flex-shrink-0">
            <IconComponent className={`h-5 w-5 ${styles.icon}`} />
          </div>
          <div className="ml-3 flex-1">
            <p className={`text-sm font-medium ${styles.text}`}>
              {message}
            </p>
          </div>
          <div className="ml-4 flex-shrink-0">
            <button
              onClick={onClose}
              className={`${styles.bg} ${styles.border} rounded-md inline-flex text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500`}
            >
              <span className="sr-only">Close</span>
              <X className="h-5 w-5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Toast;
