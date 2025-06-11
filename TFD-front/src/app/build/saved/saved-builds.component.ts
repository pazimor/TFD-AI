import { Component, inject, signal, WritableSignal, OnInit, effect, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { loginStore } from '../../store/login.store';
import { buildStore } from '../../store/build.store';
import { patchState } from '@ngrx/signals';
import { BuildCardComponent, BuildSummary } from './build-card/build-card.component';
import { environment } from '../../../env/environment';
import { Router } from '@angular/router';
import { buildListStore } from '../../store/build-list.store'; // For navigation

@Component({
  selector: 'saved-builds-list',
  imports: [CommonModule, BuildCardComponent], // BuildCardComponent added
  templateUrl: './saved-builds.component.html',
  styleUrls: ['./saved-builds.component.scss']
})
export class SavedBuildsListComponent {
  private buildListStore = inject(buildListStore)
  private loginStore = inject(loginStore);
  private buildStore = inject(buildStore);
  //private router = inject(Router); // TODO: not use full now

  builds: WritableSignal<BuildSummary[]> = signal([]);
  isLoading = signal(false);
  errorLoading = signal<string | null>(null);

  constructor() {
    effect(() => {
      if (this.loginStore.loggedIn()) {
        const userId = this.loginStore.user()?.id;
        if (userId!) {
          this.buildListStore.load(userId)
        }
      }
    });

    effect(() => {
      if (this.buildListStore.resource.hasValue()) {
        this.builds.set(this.buildListStore.resource.value());
      }
    });
  }

  LoadBuild(buildId: number): void {
    this.buildStore.loadFromApi(buildId);
    // TODO: navigate to the builder view if needed
  }

  refresh(): void {
    this.buildListStore.resource.reload()
  }
}
