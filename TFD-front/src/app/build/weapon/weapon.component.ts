import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import {ModuleBuildComponent} from '../module/module.component';

@Component({
  standalone: true,
  selector: 'weapon-build',
  imports: [CommonModule, ModuleBuildComponent],
  templateUrl: './weapon.component.html',
  styleUrls: ['./weapon.component.scss', '../main/main.component.scss' ,'../../../styles.scss']
})
export class WeaponBuildComponent {

  constructor() {}
}
