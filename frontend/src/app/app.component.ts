import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';
import { Store } from '@ngrx/store';
import { Observable } from 'rxjs';

import { AppState } from './store/app.state';
import { selectIsAuthenticated, selectCurrentUser } from './store/auth/auth.selectors';
import { HeaderComponent } from './shared/components/header/header.component';
import { FooterComponent } from './shared/components/footer/footer.component';
import { LoadingSpinnerComponent } from './shared/components/loading-spinner/loading-spinner.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    CommonModule,
    RouterOutlet,
    HeaderComponent,
    FooterComponent,
    LoadingSpinnerComponent
  ],
  template: `
    <div class="app-container">
      <app-header *ngIf="isAuthenticated$ | async"></app-header>
      
      <main class="main-content" [class.with-header]="isAuthenticated$ | async">
        <router-outlet></router-outlet>
      </main>
      
      <app-footer *ngIf="isAuthenticated$ | async"></app-footer>
      
      <app-loading-spinner></app-loading-spinner>
    </div>
  `,
  styles: [`
    .app-container {
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }
    
    .main-content {
      flex: 1;
      padding: 0;
    }
    
    .main-content.with-header {
      padding-top: 60px;
    }
    
    @media (max-width: 768px) {
      .main-content.with-header {
        padding-top: 50px;
      }
    }
  `]
})
export class AppComponent implements OnInit {
  isAuthenticated$: Observable<boolean>;
  currentUser$: Observable<any>;

  constructor(private store: Store<AppState>) {
    this.isAuthenticated$ = this.store.select(selectIsAuthenticated);
    this.currentUser$ = this.store.select(selectCurrentUser);
  }

  ngOnInit(): void {
    // Initialize app
    console.log('🚀 MentorMind AI Learning Platform initialized');
  }
}
