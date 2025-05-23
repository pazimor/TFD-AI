import {Component, computed, inject, input, InputSignal, signal, Signal, ViewChild} from '@angular/core';
import { CommonModule } from '@angular/common';
import { dataStore } from '../store/data.store';
import { visualStore, Selector } from '../store/display.store';
import { LoginDialogComponent } from '../auth/login-dialog/login-dialog.component';



@Component({
  imports: [CommonModule, LoginDialogComponent],
  selector: 'sidebar',
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.scss']
})
export class sidebarComponent {
  readonly data_store = inject(dataStore);
  readonly visual_store = inject(visualStore);

  isOpen = this.visual_store.isSidebarOpen;

  toggleSidebar() {
    this.visual_store.set_sidebar(!this.isOpen());
  }

  protected readonly Selector = Selector;
}
