import { Component, inject, Input, computed } from '@angular/core';

import { MatDialog } from '@angular/material/dialog';
import { selectorComponent } from '../selector/selector.component';
import { buildStore } from '../../store/build.store';
import { selectorData } from '../../types/selector.types';
import { ExternalComponent as Ext, defaultExternalComponent } from '../../types/external.types';
import { ExternalDisplayComponent } from './display/external-display.component';
import { defaultWeapon } from '../../types/weapon.types';
import { dataStore } from '../../store/data.store';

@Component({
  standalone: true,
  selector: 'external-build',
  imports: [ExternalDisplayComponent],
  templateUrl: './external.component.html',
  styleUrls: ['./external.component.scss', '../main/main.component.scss']
})
export class ExternalBuildComponent {
  readonly build_store = inject(buildStore);
  readonly data_store = inject(dataStore);
  @Input() index = 0;

  external = computed(() => this.build_store.externals()[this.index]);

  externalData: selectorData = {
    selectitems: 'externals',
    filterClass: 0,
    descendant: undefined
  };

  constructor(private dialog: MatDialog) {}

  openDialog(): void {
    const dialogRef = this.dialog.open(selectorComponent, {
      autoFocus: true,
      data: this.externalData
    });

    dialogRef.afterClosed().subscribe((id: number) => {
      if (id === undefined) {
        id = 0;
      }
      const res = this.data_store.externalResource.value()
        ?.filter(des => des.external_component_id === id)[0]
        ?? defaultExternalComponent
      this.build_store.setExternal(this.index, res);
    });
  }
}
