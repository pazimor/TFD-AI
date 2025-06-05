import { Component, inject, computed, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import {ModuleBuildComponent} from '../module/module.component';
import { selectorData } from '../../types/selector.types';
import { WeaponDisplayComponent } from './display/weapon-display.component';
import { selectorComponent } from '../selector/selector.component';
import { MatDialog } from '@angular/material/dialog';
import { defaultWeapon, WeaponResponse } from '../../types/weapon.types';
import { ModuleResponse } from '../../types/module.types';
import { buildStore } from '../../store/build.store';

@Component({
  standalone: true,
  selector: 'weapon-build',
  imports: [CommonModule, ModuleBuildComponent, WeaponDisplayComponent],
  templateUrl: './weapon.component.html',
  styleUrls: ['./weapon.component.scss', '../main/main.component.scss' ,'../../../styles.scss']
})
export class WeaponBuildComponent {
  @Input() index = 0;
  readonly build_store = inject(buildStore);

  weapon = computed(() => this.build_store.weapons()[this.index]);
  modules = computed(() => this.build_store.weaponsModules()[this.index]);

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

  handleModuleSelected(index: number, module: ModuleResponse) {
    this.build_store.updateWeaponModule(this.index, index, module);
  }

  openDialog(): void {

    const dialogRef = this.dialog.open(selectorComponent, {
      autoFocus: true,
      data: this.weapon_data
    });
    dialogRef.afterClosed().subscribe((res: WeaponResponse) => {
      if (res === undefined) {
        res = defaultWeapon;
      }
      this.build_store.setWeaponAt(this.index, res);
      //TODO: make a fonction cause some weapons are not working and somtime there is incompatibles mods showing up
      this.module_data.filterClass = res.weapon_rounds_type_id
    });
  }

}
