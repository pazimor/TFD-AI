import {Component, inject, input, InputSignal} from '@angular/core';
import {appStore, Selector} from '../store/data.store'
import {CommonModule} from '@angular/common';
import {Character} from './character.model';

@Component({
  imports: [CommonModule],
  selector: 'character',
  templateUrl: './character.component.html',
  styleUrls: ['./character.component.scss']
})
export class CharacterComponent {
  readonly store = inject(appStore);

  readonly selector = this.store.selector();
  readonly character: InputSignal<Character> = input.required<Character>();
  readonly smallview: InputSignal<boolean> = input.required<boolean>()

  language$$ = this.store.language

  clickedOn(): void {
    if(this.selector === Selector.CHARACTERE) {
      this.store.set_selectedDescendant(this.character().id)
      this.store.set_selector(Selector.DEFAULT)
    } else {
      this.store.set_selector(Selector.CHARACTERE)
    }
  }
}
