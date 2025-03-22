import { Component, inject, input, InputSignal } from '@angular/core';
import { dataStore } from '../store/data.store'
import { CommonModule } from '@angular/common';
import { Character } from './character.model';
import { visualStore, Selector } from '../store/display.store';

@Component({
  imports: [CommonModule],
  selector: 'character',
  templateUrl: './character.component.html',
  styleUrls: ['./character.component.scss']
})
export class CharacterComponent {
  readonly data_store = inject(dataStore);
  readonly visual_store = inject(visualStore);

  readonly selector = this.visual_store.selector();
  readonly character: InputSignal<Character> = input.required<Character>();
  readonly smallview: InputSignal<boolean> = input.required<boolean>()

  language$$ = this.visual_store.language

  clickedOn(): void {
    if(this.selector === Selector.CHARACTERE) {
      this.data_store.set_selectedDescendant(this.character().id)
      this.visual_store.set_selector(Selector.DEFAULT)
    } else {
      this.visual_store.set_selector(Selector.CHARACTERE)
    }
  }
}
