import { Component, computed, inject, input, InputSignal } from '@angular/core';
import { dataStore } from '../store/data.store'
import { CommonModule } from '@angular/common';
import { Weapon } from './weapon.model';
import { visualStore, Selector } from '../store/display.store';

@Component({
  imports: [CommonModule],
  selector: 'weapon',
  templateUrl: './weapon.component.html',
  styleUrls: ['./weapon.component.scss']
})
export class WeaponComponent {
  readonly data_store = inject(dataStore);
  readonly visual_store = inject(visualStore);

  readonly selector: InputSignal<Selector> = input.required<Selector>();
  readonly weapon: InputSignal<Weapon> = input.required<Weapon>();
  readonly smallview: InputSignal<boolean> = input.required<boolean>()

  weaponImg$$ = computed(() => this.weapon()?.display_data.img)
  language$$ = this.visual_store.language

  clickedOn(): void {
    if(this.selector() !== Selector.DEFAULT && this.selector() !== this.visual_store.selector()) {
      this.visual_store.set_selector(this.selector())
    } else if (this.selector() === this.visual_store.selector()) {
      //change weapon
      this.data_store.set_weapon(this.weapon().id, + this.selector().charAt(6) - 1 )
      this.visual_store.set_selector(Selector.DEFAULT)
    }
  }

}
