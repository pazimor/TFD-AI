import { Component, computed, inject, input, InputSignal} from '@angular/core';
import { appStore } from '../store/data.store'
import { CommonModule } from '@angular/common';
import { Weapon } from './weapon.model';

@Component({
  imports: [CommonModule],
  selector: 'weapon',
  templateUrl: './weapon.component.html',
  styleUrls: ['./weapon.component.scss']
})
export class WeaponComponent {
  readonly store = inject(appStore);

  readonly weapon: InputSignal<Weapon> = input.required<Weapon>();
  readonly smallview: InputSignal<boolean> = input.required<boolean>()

  weaponImg$$ = computed(() => this.weapon()?.display_data.img)
  language$$ = this.store.language

}
