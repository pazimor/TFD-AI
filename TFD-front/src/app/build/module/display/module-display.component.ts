import { Component, inject, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { dataStore, defaultTranslate, TranslationString } from '../../../store/data.store';
import { ModuleResponse } from '../../../types/module.types';

@Component({
  standalone: true,
  selector: 'module',
  imports: [CommonModule],
  templateUrl: './module-display.component.html',
  styleUrls: ['./module-display.component.scss']
})
export class ModuleComponent {
  constructor() {}

  readonly data_store = inject(dataStore);

  @Input() module!: ModuleResponse;

  get_translate(id: number): TranslationString {
    if (this.data_store.translationResource.hasValue()) {
      return this.data_store.translationResource.value()[id-1]
    } else {
      return defaultTranslate
    }
  }

  get name(): string {
    return this.get_translate(this.module.module_name_id)?.fr ?? '';
  }
}
