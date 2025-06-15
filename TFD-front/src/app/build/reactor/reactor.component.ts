import { Component, inject } from '@angular/core';

import { MatDialog } from '@angular/material/dialog';
import { selectorComponent } from '../selector/selector.component';
import { buildStore } from '../../store/build.store';
import { selectorData } from '../../types/selector.types';
import { Reactor, defaultReactor } from '../../types/reactor.types';
import { ReactorDisplayComponent } from './display/reactor-display.component';
import { defaultModule } from '../../types/module.types';
import { dataStore } from '../../store/data.store';

@Component({
  standalone: true,
  selector: 'reactor-build',
  imports: [ReactorDisplayComponent],
  templateUrl: './reactor.component.html',
  styleUrls: ['./reactor.component.scss', '../main/main.component.scss']
})
export class ReactorBuildComponent {
  readonly data_store = inject(dataStore);
  readonly build_store = inject(buildStore);
  reactor = this.build_store.reactor;

  reactorData: selectorData = {
    selectitems: 'reactors',
    filterClass: 0,
    descendant: undefined
  };

  constructor(private dialog: MatDialog) {}

  openDialog(): void {
    const dialogRef = this.dialog.open(selectorComponent, {
      autoFocus: true,
      data: this.reactorData
    });

    dialogRef.afterClosed().subscribe((id: number) => {
      if (id === undefined) {
        id = 0;
      }
      const res = this.data_store.reactorResource.value()
        ?.filter(rea => rea.reactor_id === id)[0]
        ?? defaultReactor

      this.build_store.setReactor(res);
    });
  }
}
