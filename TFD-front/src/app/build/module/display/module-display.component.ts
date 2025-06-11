import { Component, inject, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { dataStore, defaultTranslate, TranslationString } from '../../../store/data.store';
import { ModuleResponse } from '../../../types/module.types';
import { visualStore } from '../../../store/display.store';
import { getTranslationField } from '../../../lang.utils';

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
  readonly visual_store = inject(visualStore);

  @Input() module!: ModuleResponse;

  get_translate(id: number): TranslationString {
    if (this.data_store.translationResource.hasValue()) {
      return this.data_store.translationResource.value()[id-1]
    } else {
      return defaultTranslate
    }
  }

  get name(): string {
    const langKey = getTranslationField(this.visual_store.get_lang());
    const translation = this.get_translate(this.module.module_name_id);
    // Guard against missing translation object or key
    const value = (translation as any)?.[langKey];
    return value ?? '';
  }
}
