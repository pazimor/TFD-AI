import { Component, Inject, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MAT_DIALOG_DATA, MatDialogModule, MatDialogRef } from '@angular/material/dialog';
import { Reactor } from '../../../types/reactor.types';
import { dataStore, defaultTranslate, TranslationString } from '../../../store/data.store';
import { visualStore } from '../../../store/display.store';
import { getTranslationField } from '../../../lang.utils';

@Component({
  standalone: true,
  selector: 'reactor-infos',
  imports: [CommonModule, MatDialogModule],
  templateUrl: './reactor-infos.component.html',
  styleUrls: ['./reactor-infos.component.scss']
})
export class ReactorInfosComponent {
  readonly data_store = inject(dataStore);
  readonly visual_store = inject(visualStore);

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: Reactor,
    private dialogRef: MatDialogRef<ReactorInfosComponent>
  ) {}

  close(): void {
    this.dialogRef.close();
  }

  get_translate(id: number): TranslationString {
    if (this.data_store.translationResource.hasValue()) {
      return this.data_store.translationResource.value()[id - 1];
    } else {
      return defaultTranslate;
    }
  }

  name(id: number): string {
    const langKey = getTranslationField(this.visual_store.get_lang());
    const translation = this.get_translate(id);
    const value = (translation as any)[langKey];
    return value ?? '';
  }
}
