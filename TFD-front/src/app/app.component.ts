import {
  Component,
  inject,
  Signal,
} from '@angular/core';

import { FormsModule } from '@angular/forms';
import { sidebarComponent } from './sidebar/sidebar.component';
import { dataStore } from './store/data.store';
import { visualStore } from './store/display.store';
import {MatTab, MatTabGroup} from '@angular/material/tabs';
import { trigger, transition, style, animate } from '@angular/animations';
import {MainBuildComponent} from './build/main/main.component';
import { SavedBuildsListComponent } from './build/saved/saved-builds.component';
import { SearchComponent } from './search/search.component';
import { getUILabel } from './lang.utils';
import { Router, NavigationEnd } from '@angular/router';
import { filter } from 'rxjs';
import { loginStore } from './store/login.store';

@Component({
  imports: [
    FormsModule,
    sidebarComponent,
    MatTab,
    MatTabGroup,
    MainBuildComponent,
    SavedBuildsListComponent,
    SearchComponent
],
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
  animations: [
    trigger('slideUpAnimation', [
      transition(':enter', [
        style({ transform: 'translateY(100%)', opacity: 0 }),
        animate('300ms ease-out', style({ transform: 'translateY(0)', opacity: 1 }))
      ]),
      transition(':leave', [
        style({ transform: 'translateY(0)', opacity: 1 }),
        animate('300ms ease-in', style({ transform: 'translateY(100%)', opacity: 0 }))
      ])
    ])
  ]
})
export class AppComponent {
  readonly data_store = inject(dataStore);
  readonly visual_store = inject(visualStore);
  readonly login_store = inject(loginStore);
  private router = inject(Router);

  title = 'TFD-front';

  selectedIndex = 0;

  isSidebarOpen$$: Signal<boolean> = this.visual_store.isSidebarOpen

  constructor() {
    this.login_store.initFromStorage();
    this.updateIndexFromUrl(this.router.url);
    this.router.events
      .pipe(filter(event => event instanceof NavigationEnd))
      .subscribe((event) => {
        this.updateIndexFromUrl((event as NavigationEnd).urlAfterRedirects);
      });
  }

  onTabChange(index: number) {
    const route =
      index === 1 ? '/my-builds' : index === 2 ? '/build-maker' : '/search';
    this.router.navigateByUrl(route);
  }

  private updateIndexFromUrl(url: string) {
    if (url.startsWith('/my-builds')) {
      this.selectedIndex = 1;
    } else if (url.startsWith('/build-maker')) {
      this.selectedIndex = 2;
    } else {
      this.selectedIndex = 0;
    }
  }

  label(key: Parameters<typeof getUILabel>[1]) {
    return getUILabel(this.visual_store.get_lang(), key);
  }
}
