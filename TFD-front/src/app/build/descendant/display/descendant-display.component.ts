import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DescendantsResponse } from '../../../types/descendant.types';  // type déjà présent

@Component({
  standalone: true,
  selector: 'descendant',
  imports: [CommonModule],
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
