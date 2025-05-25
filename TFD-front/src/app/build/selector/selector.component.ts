import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { dataStore } from '../../store/data.store';
import { ModuleComponent } from '../module/display/module-display.component';
import { MatDialogModule } from '@angular/material/dialog';

@Component({
  standalone: true,
  selector: 'selector',
  imports: [CommonModule, ModuleComponent, MatDialogModule],
  templateUrl: './selector.component.html',
  styleUrls: ['./selector.component.scss', '../../../styles.scss']
})
export class selectorComponent {
  //Todo: store for items / descendant / module to fill
  readonly data_store = inject(dataStore);

  constructor() {
    this.data_store.load_modules()
    this.data_store.load_translations()
  }

  test() {
    console.log(this.data_store.modulesResource?.hasValue())
  }
}
