import {Component, inject, input, InputSignal} from '@angular/core';
import { appStore } from '../store/data.store'
import { CommonModule } from '@angular/common';
import {Character} from './character.model';

@Component({
  imports: [CommonModule],
  selector: 'character',
  templateUrl: './character.component.html',
  styleUrls: ['./character.component.scss']
})
export class CharacterComponent {
  readonly store = inject(appStore);

  readonly character: InputSignal<Character> = input.required<Character>();
  readonly smallview: InputSignal<boolean> = input.required<boolean>()

  language$$ = this.store.language

  clickedOn():void {
    if (this.store.selectedDescendant() === 0) {
      this.store.set_selectedDescendant(this.character().id)
    } else {
      this.store.set_selectedDescendant(0)
    }
  }
}
