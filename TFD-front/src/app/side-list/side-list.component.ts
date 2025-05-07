import {Component, inject, input, InputSignal, signal, Signal, ViewChild} from '@angular/core';
import { CommonModule } from '@angular/common';
import { dataStore, } from '../store/data.store';
import { visualStore, Selector} from '../store/display.store';

@Component({
  imports: [CommonModule],
  selector: 'side-list',
  templateUrl: './side-list.component.html',
  styleUrls: ['./side-list.component.scss']
})
export class sideListComponent {
  readonly data_store = inject(dataStore);
  readonly visual_store = inject(visualStore);

  selection$$: Signal<Selector> = this.visual_store.selector;

  isOpen = this.visual_store.isSidebarOpen;
}
