import {
  Component, computed,
  inject,
  Signal,
  ViewChild,
} from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { LanguageListComponent } from './langlist/language-list.component';
import { sidebarComponent } from './sidebar/sidebar.component';
import { dataStore } from './store/data.store';
import { visualStore } from './store/display.store';
import {MatTab, MatTabGroup} from '@angular/material/tabs';
import { trigger, transition, style, animate } from '@angular/animations';
import {MainBuildComponent} from './build/main/main.component';
import { SavedBuildsComponent } from './build/saved/saved-builds.component';


@Component({
  imports: [CommonModule, FormsModule, sidebarComponent, MatTab, MatTabGroup, MainBuildComponent, SavedBuildsComponent],
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

  title = 'TFD-front';

  selectedIndex = 0;

  isSidebarOpen$$: Signal<boolean> = this.visual_store.isSidebarOpen
}
