import {
  Component, computed,
  inject,
  Signal,
  ViewChild,
} from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { BuildComponent } from './build/build.component';
import { LanguageListComponent } from './langlist/language-list.component';
import { ModuleBankComponent } from './module-bank/module-bank.component';
import {sidebarComponent} from './sidebar/sidebar.component';
import { appStore } from './store/data.store';
import { MatTab, MatTabGroup } from '@angular/material/tabs';
import { trigger, transition, style, animate } from '@angular/animations';


@Component({
  imports: [CommonModule, FormsModule, BuildComponent, LanguageListComponent, ModuleBankComponent, LanguageListComponent, sidebarComponent, MatTab, MatTabGroup],
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
  @ViewChild(BuildComponent) buildComponent!: BuildComponent;
  @ViewChild(LanguageListComponent) languageListComponent!: LanguageListComponent;
  @ViewChild(ModuleBankComponent) moduleBankComponent!: ModuleBankComponent;

  readonly store = inject(appStore);
  title = 'TFD-front';

  language$$ = this.store.language

  selectedIndex = 0;

  current_character$$ = computed(() => {
    const selectedId = this.store.selectedDescendant();
    const characters = this.store.descendants();
    return characters.find(character => character.id === selectedId) || characters[0];
  });

  current_weapons$$ = computed(() => {
    const selectedWeaponIds = this.store.selectedWeapons();
    const weapons = this.store.weapons();
    return selectedWeaponIds.map(id => weapons.find(weapon => weapon.id === id) || weapons[0]);
  });

  isSidebarOpen$$: Signal<boolean> = this.store.isSidebarOpen
}
