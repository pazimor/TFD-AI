import {Component, inject, input, InputSignal, Signal, ViewChild} from '@angular/core';
import { CommonModule } from '@angular/common';
import { CharacterComponent } from '../character/character.component';
import { appStore } from '../store/data.store';
import { Character } from '../character/character.model';



@Component({
  imports: [CommonModule, CharacterComponent],
  selector: 'sidebar',
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.scss']
})
export class sidebarComponent {
  readonly store = inject(appStore);

  @ViewChild(CharacterComponent) characterComponent!: CharacterComponent;

  selected$$: Signal<number> = this.store.selectedDescendant
  characters$$: Signal<Character[]> = this.store.descendants;

  isOpen = false;

  toggleSidebar() {
    this.isOpen = !this.isOpen;
  }
}
