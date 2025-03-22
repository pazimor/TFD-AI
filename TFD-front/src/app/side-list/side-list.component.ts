import {Component, inject, input, InputSignal, signal, Signal, ViewChild} from '@angular/core';
import { CommonModule } from '@angular/common';
import { CharacterComponent } from '../character/character.component';
import { WeaponComponent } from '../weapon/weapon.component';
import { dataStore, } from '../store/data.store';
import { Character } from '../character/character.model';
import { Weapon } from '../weapon/weapon.model';
import { visualStore, Selector} from '../store/display.store';



@Component({
  imports: [CommonModule, CharacterComponent, WeaponComponent],
  selector: 'side-list',
  templateUrl: './side-list.component.html',
  styleUrls: ['./sidelist.component.scss']
})
export class sideListComponent {
  readonly data_store = inject(dataStore);
  readonly visual_store = inject(visualStore);

  @ViewChild(CharacterComponent) characterComponent!: CharacterComponent;
  @ViewChild(WeaponComponent) weaponComponent!: WeaponComponent;

  selection$$: Signal<Selector> = this.visual_store.selector;

  characters$$: Signal<Character[]> = this.data_store.descendants_available;
  weapon$$: Signal<Weapon[]> = this.data_store.weapons_available;

  isOpen = this.visual_store.isSidebarOpen;
}
