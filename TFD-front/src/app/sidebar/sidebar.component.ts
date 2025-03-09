import {Component, computed, inject, input, InputSignal, signal, Signal, ViewChild} from '@angular/core';
import { CommonModule } from '@angular/common';
import { CharacterComponent } from '../character/character.component';
import { WeaponComponent } from '../weapon/weapon.component';
import {appStore, Selector} from '../store/data.store';
import { Character } from '../character/character.model';
import {Weapon} from '../weapon/weapon.model';
import { sideListComponent } from '../side-list/side-list.component';



@Component({
  imports: [CommonModule, CharacterComponent, WeaponComponent, sideListComponent],
  selector: 'sidebar',
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.scss']
})
export class sidebarComponent {
  readonly store = inject(appStore);

  @ViewChild(CharacterComponent) characterComponent!: CharacterComponent;
  @ViewChild(WeaponComponent) weaponComponent!: WeaponComponent;

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

  isOpen = this.store.isSidebarOpen;

  toggleSidebar() {
    this.store.set_sidebar(!this.isOpen());
  }

  protected readonly Selector = Selector;
}
