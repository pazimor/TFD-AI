import { Component, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import {ModuleBuildComponent} from '../module/module.component';
import { selectorData } from '../../types/selector.types';
import { WeaponDisplayComponent } from './display/weapon-display.component';
import { selectorComponent } from '../selector/selector.component';
import { MatDialog } from '@angular/material/dialog';
import { defaultWeapon, WeaponResponse } from '../../types/weapon.types';

@Component({
  standalone: true,
  selector: 'weapon-build',
  imports: [CommonModule, ModuleBuildComponent, WeaponDisplayComponent],
  templateUrl: './weapon.component.html',
  styleUrls: ['./weapon.component.scss', '../main/main.component.scss' ,'../../../styles.scss']
})
export class WeaponBuildComponent {

  weapon = signal<WeaponResponse>(defaultWeapon);

  weapon_data: selectorData = {
    selectitems: "weapons",
    filterClass: 890,
    descendant: undefined
  }

  module_data: selectorData = {
    selectitems: "modules",
    filterClass: 0,
    descendant: undefined
  }

  constructor(private dialog: MatDialog,) {}

  openDialog(): void {

    const dialogRef = this.dialog.open(selectorComponent, {
      autoFocus: true,
      data: this.weapon_data
    });
    dialogRef.afterClosed().subscribe((res: WeaponResponse) => {
      if (res === undefined) {
        res = defaultWeapon;
      }
      this.weapon.set(res);
      //TODO: make a fonction cause some weapons are not working and somtime there is incompatibles mods showing up
      this.module_data.filterClass = res.weapon_rounds_type_id
    });
  }

}
