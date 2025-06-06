import { Component, Input, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SavedBuild } from '../../types/build.types';
import { buildStore } from '../../store/build.store';

@Component({
  standalone: true,
  selector: 'build-card',
  imports: [CommonModule],
  template: `<div class="build-card" (click)="select()">{{ build.build_name }}</div>`,
  styleUrls: ['./build-card.component.scss']
})
export class BuildCardComponent {
  @Input() build!: SavedBuild;
  readonly store = inject(buildStore);

  select() {
    if (this.build) {
      this.store.loadFromApi(this.build.build_id);
    }
  }
}
