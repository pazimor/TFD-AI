import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ExternalComponent } from '../../../types/external.types';

@Component({
  standalone: true,
  selector: 'external',
  imports: [CommonModule],
  templateUrl: './external-display.component.html',
  styleUrls: ['./external-display.component.scss']
})
export class ExternalDisplayComponent {
  @Input() external!: ExternalComponent;

  get imageUrl(): string {
    return this.external?.image_url ?? '';
  }
}
