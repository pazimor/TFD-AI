import {Component, inject, input, InputSignal} from '@angular/core';
import {DragDropModule} from '@angular/cdk/drag-drop';
import { Module } from './module.model';
import { CommonModule } from '@angular/common';
import { appStore } from '../store/data.store';

@Component({
  imports: [CommonModule, DragDropModule],
  selector: 'Module-item',
  templateUrl: './module.component.html',
  styleUrls: ['./module.component.scss', './modules-tiers.scss']
})
export class ModuleComponent {
  readonly currentModule: InputSignal<Module> = input.required<Module>()
  readonly store = inject(appStore);

  // Initialisez un tableau pour les objets sélectionnés
  language$$ = this.store.language;
}
