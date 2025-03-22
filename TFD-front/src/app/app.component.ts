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
import { sidebarComponent } from './sidebar/sidebar.component';
import { dataStore } from './store/data.store';
import { visualStore } from './store/display.store';
import {MatTab, MatTabChangeEvent, MatTabGroup} from '@angular/material/tabs';
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

  readonly data_store = inject(dataStore);
  readonly visual_store = inject(visualStore);

  title = 'TFD-front';

  language$$ = this.visual_store.language

  selectedIndex = 0;

  select_type(event: MatTabChangeEvent) {
    const index = event.index;
    if (index === 1) {
      this.visual_store.set_displayOnly("Légataire");
    } else if (index === 2) {
      const weapon = this.data_store.weapons_available()
        .find(weapon => weapon.id === this.data_store.selected_weapon_1().weapon_id)
      this.visual_store.set_displayOnly(weapon?.type ?? "");
    } else if (index === 3) {
      const weapon = this.data_store.weapons_available()
        .find(weapon => weapon.id === this.data_store.selected_weapon_2().weapon_id)
      this.visual_store.set_displayOnly(weapon?.type ?? "");
    } else if (index === 4) {
      const weapon = this.data_store.weapons_available()
        .find(weapon => weapon.id === this.data_store.selected_weapon_3().weapon_id)
      this.visual_store.set_displayOnly(weapon?.type ?? "");
    }
  }

  current_character$$ = computed(() => {
    const selectedId = this.data_store.selected_descendant().descendant_id;
    const characters = this.data_store.descendants_available();
    return characters.find(character => character.id === selectedId) || characters[0];
  });

  current_weapon_1$$ = computed(() => {
    const selectedWeaponId = this.data_store.selected_weapon_1();
    const weapons = this.data_store.weapons_available();
    return weapons.find(weapon => weapon.id === selectedWeaponId.weapon_id) || weapons[0];
  });

  current_weapon_2$$ = computed(() => {
    const selectedWeaponId = this.data_store.selected_weapon_2();
    const weapons = this.data_store.weapons_available();
    return weapons.find(weapon => weapon.id === selectedWeaponId.weapon_id) || weapons[0];
  });

  current_weapon_3$$ = computed(() => {
    const selectedWeaponId = this.data_store.selected_weapon_3();
    const weapons = this.data_store.weapons_available();
    return weapons.find(weapon => weapon.id === selectedWeaponId.weapon_id) || weapons[0];
  });

  isSidebarOpen$$: Signal<boolean> = this.visual_store.isSidebarOpen
}
