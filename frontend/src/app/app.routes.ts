import { Routes } from '@angular/router';
import { authGuard } from './core/guards/auth.guard';

export const routes: Routes = [
  {
    path: '',
    redirectTo: '/dashboard',
    pathMatch: 'full'
  },
  {
    path: 'auth',
    loadChildren: () => import('./features/auth/auth.routes').then(m => m.AUTH_ROUTES)
  },
  {
    path: 'dashboard',
    loadChildren: () => import('./features/dashboard/dashboard.routes').then(m => m.DASHBOARD_ROUTES),
    canActivate: [authGuard]
  },
  {
    path: 'quizzes',
    loadChildren: () => import('./features/quizzes/quiz.routes').then(m => m.QUIZ_ROUTES),
    canActivate: [authGuard]
  },
  {
    path: 'ai-tutor',
    loadChildren: () => import('./features/ai-tutor/ai-tutor.routes').then(m => m.AI_TUTOR_ROUTES),
    canActivate: [authGuard]
  },
  {
    path: 'performance',
    loadChildren: () => import('./features/performance/performance.routes').then(m => m.PERFORMANCE_ROUTES),
    canActivate: [authGuard]
  },
  {
    path: 'gamification',
    loadChildren: () => import('./features/gamification/gamification.routes').then(m => m.GAMIFICATION_ROUTES),
    canActivate: [authGuard]
  },
  {
    path: 'profile',
    loadChildren: () => import('./features/profile/profile.routes').then(m => m.PROFILE_ROUTES),
    canActivate: [authGuard]
  },
  {
    path: '**',
    redirectTo: '/dashboard'
  }
];
