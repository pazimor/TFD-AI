import { Component, inject, signal, WritableSignal, OnInit, effect } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { loginStore } from '../../store/login.store';
import { BuildCardComponent, BuildSummary } from './build-card/build-card.component';
import { environment } from '../../../env/environment';
import { Router } from '@angular/router'; // For navigation

@Component({
  selector: 'saved-builds-list',
  imports: [CommonModule, BuildCardComponent], // BuildCardComponent added
  templateUrl: './saved-builds.component.html',
  styleUrls: ['./saved-builds.component.scss']
})
export class SavedBuildsListComponent implements OnInit {
  private http = inject(HttpClient);
  private loginStore = inject(loginStore);
  private router = inject(Router); // For navigation

  builds: WritableSignal<BuildSummary[]> = signal([]);
  isLoading = signal(false);
  errorLoading = signal<string | null>(null);

  constructor() {
    // Effect to react to login state changes (e.g., user logs out, clear builds)
    effect(() => {
      if (!this.loginStore.loggedIn()) {
        this.builds.set([]);
        this.errorLoading.set(null);
        // Optionally redirect to login or home page
      } else {
        // If user logs in and builds are not loaded, load them.
        // This handles cases where component might initialize before login completes.
        if (this.builds().length === 0 && !this.isLoading() && !this.errorLoading()) {
          // this.fetchBuilds(); // ngOnInit will call this initially
        }
      }
    });
  }

  ngOnInit(): void {
    if (this.loginStore.loggedIn()) {
      this.fetchBuilds();
    } else {
      this.errorLoading.set('User not logged in. Please log in to see your builds.');
      // Consider redirecting to login page or showing a login prompt
    }
  }

  fetchBuilds(): void {
    const userId = this.loginStore.user()?.id;
    if (!userId) {
      this.errorLoading.set('User ID not found. Cannot fetch builds.');
      return;
    }

    this.isLoading.set(true);
    this.errorLoading.set(null);
    const apiUrl = `${environment.apiBaseUrl}/api/builds?user_google_id=${userId}`;

    this.http.get<{ success: boolean, builds: BuildSummary[], error?: string }>(apiUrl)
      .subscribe({
        next: (response) => {
          if (response.success) {
            this.builds.set(response.builds);
          } else {
            this.errorLoading.set(response.error || 'Failed to load builds.');
            this.builds.set([]);
          }
          this.isLoading.set(false);
        },
        error: (err: HttpErrorResponse) => {
          console.error('Error fetching builds:', err);
          this.errorLoading.set(err.error?.error || err.message || 'An unknown error occurred while fetching builds.');
          this.builds.set([]);
          this.isLoading.set(false);
        }
      });
  }

  handleViewBuild(buildId: number): void {
    console.log('View build requested for ID:', buildId);
    // Next subtask: Fetch full build and navigate/pass data to Build Maker
    // For now, just log.
    // Example navigation (will be fleshed out in next step):
    // this.router.navigate(['/build-maker'], { state: { loadBuildId: buildId } });
    alert(`Build card clicked for build ID: ${buildId}. Loading logic to be implemented in next step.`);
  }
}
