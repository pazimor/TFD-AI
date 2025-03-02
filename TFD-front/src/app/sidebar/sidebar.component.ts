import {Component, inject, input, InputSignal, signal, Signal, ViewChild} from '@angular/core';
import { CommonModule } from '@angular/common';
import { CharacterComponent } from '../character/character.component';
import { WeaponComponent } from '../weapon/weapon.component';
import { appStore } from '../store/data.store';
import { Character } from '../character/character.model';
import {Weapon} from '../weapon/weapon.model';
import {defaultModule, Module} from '../module/module.model';



@Component({
  imports: [CommonModule, CharacterComponent, WeaponComponent],
  selector: 'sidebar',
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.scss']
})
export class sidebarComponent {
  readonly store = inject(appStore);

  @ViewChild(CharacterComponent) characterComponent!: CharacterComponent;
  @ViewChild(WeaponComponent) weaponComponent!: WeaponComponent;

  selected$$: Signal<number> = this.store.selectedDescendant
  characters$$: Signal<Character[]> = this.store.descendants;
  weapon$$: Signal<Weapon[]> = this.store.weapons;

  isOpen = this.store.isSidebarOpen;

  toggleSidebar() {
    this.store.set_sidebar(!this.isOpen());
  }
}
