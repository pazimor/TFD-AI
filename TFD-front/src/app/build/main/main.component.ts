import { Component, signal, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { WeaponBuildComponent } from '../weapon/weapon.component';
import { DescedantBuildComponent } from '../descendant/descendant.component';

@Component({
  standalone: true,
  selector: 'main-build',
  imports: [CommonModule, WeaponBuildComponent, DescedantBuildComponent],
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.scss', '../../../styles.scss']
})
export class MainBuildComponent {

  constructor() {}

  weapons = signal<number>(0);
  descendants = signal<number>(0);

  // convenience computed signal that yields an array of length `weapons()`
  weaponRange = computed(() => Array.from({ length: this.weapons() }));

  addWeapon() { this.weapons.update(v => Math.min(3, v + 1)); }
  removeWeapon() { this.weapons.update(v => Math.max(0, v - 1)); }

  addDescendant() { this.descendants.update(v => Math.min(1, v + 1)); }
  removeDescendant() { this.descendants.update(v => Math.max(0, v - 1)); }

  saveBuild() {
    // TODO: hook real persistence logic here
    console.log('Save build clicked');
  }
}
