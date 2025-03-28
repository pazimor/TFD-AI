import {Component, computed, inject, input, InputSignal, signal, Signal, ViewChild} from '@angular/core';
import { CommonModule } from '@angular/common';
import { CharacterComponent } from '../character/character.component';
import { WeaponComponent } from '../weapon/weapon.component';
import { dataStore } from '../store/data.store';
import { sideListComponent } from '../side-list/side-list.component';
import { visualStore, Selector } from '../store/display.store';



@Component({
  imports: [CommonModule, CharacterComponent, WeaponComponent, sideListComponent],
  selector: 'sidebar',
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.scss']
})
export class sidebarComponent {
  readonly data_store = inject(dataStore);
  readonly visual_store = inject(visualStore);

  @ViewChild(CharacterComponent) characterComponent!: CharacterComponent;
  @ViewChild(WeaponComponent) weaponComponent!: WeaponComponent;

  //duplicate function
  current_character$$ = computed(() => {
    const selectedId = this.data_store.selected_descendant().descendant_id;
    const characters = this.data_store.descendants_available();
    return characters.find(character => character.id === selectedId) || characters[0];
  });

  //duplicate fonction
  current_weapon_1$$ = computed(() => {
    const selectedWeaponId = this.data_store.selected_weapon_1().weapon_id;
    const weapons = this.data_store.weapons_available();
    return weapons.find(weapon => weapon.id === selectedWeaponId) || weapons[0];
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

  isOpen = this.visual_store.isSidebarOpen;

  toggleSidebar() {
    this.visual_store.set_sidebar(!this.isOpen());
  }

  protected readonly Selector = Selector;
}
