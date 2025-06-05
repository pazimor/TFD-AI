import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Reactor } from '../../../types/reactor.types';

@Component({
  standalone: true,
  selector: 'reactor',
  imports: [CommonModule],
  templateUrl: './reactor-display.component.html',
  styleUrls: ['./reactor-display.component.scss']
})
export class ReactorDisplayComponent {
  @Input() reactor!: Reactor;

  get imageUrl(): string {
    return this.reactor?.image_url ?? '';
  }
}
