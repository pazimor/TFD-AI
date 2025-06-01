import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { WeaponResponse } from '../../../types/weapon.types';

@Component({
  standalone: true,
  selector: 'weapon',
  imports: [CommonModule],
  templateUrl: './weapon-display.component.html',
  styleUrls: ['./weapon-display.component.scss']
})
export class WeaponDisplayComponent {
  @Input() weapon!: WeaponResponse

  constructor() {}

  get imageUrl(): string {
    return this.weapon.image_url ?? '';
  }
}
