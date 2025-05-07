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


@Component({
  imports: [CommonModule, FormsModule, LanguageListComponent, LanguageListComponent, sidebarComponent, MatTab, MatTabGroup],
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
  @ViewChild(LanguageListComponent) languageListComponent!: LanguageListComponent;

  readonly data_store = inject(dataStore);
  readonly visual_store = inject(visualStore);

  title = 'TFD-front';

  language$$ = this.visual_store.language

  selectedIndex = 0;

  isSidebarOpen$$: Signal<boolean> = this.visual_store.isSidebarOpen
}
