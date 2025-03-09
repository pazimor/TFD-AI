import {Component, inject, input, InputSignal, signal, Signal, ViewChild} from '@angular/core';
import { CommonModule } from '@angular/common';
import { CharacterComponent } from '../character/character.component';
import { WeaponComponent } from '../weapon/weapon.component';
import { appStore, Selector } from '../store/data.store';
import { Character } from '../character/character.model';
import { Weapon } from '../weapon/weapon.model';



@Component({
  imports: [CommonModule, CharacterComponent, WeaponComponent],
  selector: 'side-list',
  templateUrl: './side-list.component.html',
  styleUrls: ['./sidelist.component.scss']
})
export class sideListComponent {
  readonly store = inject(appStore);

  @ViewChild(CharacterComponent) characterComponent!: CharacterComponent;
  @ViewChild(WeaponComponent) weaponComponent!: WeaponComponent;

  selection$$: Signal<Selector> = this.store.selector;

  characters$$: Signal<Character[]> = this.store.descendants;
  weapon$$: Signal<Weapon[]> = this.store.weapons;

  isOpen = this.store.isSidebarOpen;
}
