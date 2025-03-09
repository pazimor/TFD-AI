import {Component, computed, inject, input, InputSignal} from '@angular/core';
import {appStore, Selector} from '../store/data.store'
import {CommonModule} from '@angular/common';
import {Weapon} from './weapon.model';

@Component({
  imports: [CommonModule],
  selector: 'weapon',
  templateUrl: './weapon.component.html',
  styleUrls: ['./weapon.component.scss']
})
export class WeaponComponent {
  readonly store = inject(appStore);

  readonly selector: InputSignal<Selector> = input.required<Selector>();
  readonly weapon: InputSignal<Weapon> = input.required<Weapon>();
  readonly smallview: InputSignal<boolean> = input.required<boolean>()

  weaponImg$$ = computed(() => this.weapon()?.display_data.img)
  language$$ = this.store.language

  clickedOn(): void {
    if(this.selector() !== Selector.DEFAULT && this.selector() !== this.store.selector()) {
      this.store.set_selector(this.selector())
    } else if (this.selector() === this.store.selector()) {
      //change weapon
      this.store.set_weapon(this.weapon().id, + this.selector().charAt(6) - 1 )
      this.store.set_selector(Selector.DEFAULT)
    }
  }

}
