import { Component, inject, signal, WritableSignal, effect } from '@angular/core';

import { loginStore } from '../../store/login.store';
import { BuildCardComponent, BuildSummary } from './build-card/build-card.component';
import { Router } from '@angular/router';
import { buildListStore } from '../../store/build-list.store';
import { visualStore } from '../../store/display.store';
import { getUILabel } from '../../lang.utils';

@Component({
  selector: 'saved-builds-list',
  imports: [BuildCardComponent], // BuildCardComponent added
  templateUrl: './saved-builds.component.html',
  styleUrls: ['./saved-builds.component.scss']
})
export class SavedBuildsListComponent {
  private buildListStore = inject(buildListStore)
  private loginStore = inject(loginStore);
  private router = inject(Router);
  private visualStore = inject(visualStore);

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
    this.router.navigate(['/build-maker'], { queryParams: { build: buildId } });
  }

  refresh(): void {
    this.buildListStore.resource.reload()
  }

  label(key: Parameters<typeof getUILabel>[1]) {
    return getUILabel(this.visualStore.get_lang(), key);
  }
}
