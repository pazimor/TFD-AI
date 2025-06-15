import { Component, Input } from '@angular/core';

import { DescendantsResponse } from '../../../types/descendant.types';  // type déjà présent

@Component({
  standalone: true,
  selector: 'descendant',
  imports: [],
  templateUrl: './descendant-display.component.html',
  styleUrls: ['./descendant-display.component.scss'],
})

export class DescendantDisplayComponent {
  /** Descendant complet retourné par l’API */
  @Input() descendant!: DescendantsResponse;

  get imageUrl(): string {
    return this.descendant?.descendant_image_url ?? '';
  }
}
