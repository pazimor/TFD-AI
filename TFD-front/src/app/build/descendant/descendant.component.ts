import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import {ModuleBuildComponent} from '../module/module.component';

@Component({
  standalone: true,
  selector: 'descendant-build',
  imports: [CommonModule, ModuleBuildComponent],
  templateUrl: './descendant.component.html',
  styleUrls: ['./descendant.component.scss', '../main/main.component.scss' ,'../../../styles.scss']
})
export class DescedantBuildComponent {

  constructor() {}
}
