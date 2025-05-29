import {Component, Inject, inject, Input} from '@angular/core';
import { CommonModule } from '@angular/common';
import {dataStore, defaultTranslate, ModuleResponse, TranslationString} from '../../store/data.store';
import { ModuleComponent } from '../module/display/module-display.component';
import {MAT_DIALOG_DATA, MatDialogModule, MatDialogRef} from '@angular/material/dialog';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { FormsModule } from '@angular/forms';

@Component({
  standalone: true,
  selector: 'selector',
  imports: [CommonModule, ModuleComponent, MatDialogModule, MatProgressSpinnerModule, FormsModule],
  templateUrl: './selector.component.html',
  styleUrls: ['./selector.component.scss', '../../../styles.scss']
})
export class selectorComponent {
  //Todo: store for items / descendant / module to fill
  readonly data_store = inject(dataStore);
  filterClass: number;

  searchText = '';
  requireDescendant = false;

  filteredModules() {
    return this.data_store.modulesResource.value()?.filter(module => {
      const matchName = !this.searchText || this.get_translate(module.module_name_id).fr?.toLowerCase().includes(this.searchText.toLowerCase());
      const matchClass = !this.filterClass || (module.module_class_id === this.filterClass);
      const matchDesc = !this.requireDescendant || module.available_descendant_id != null;
      return matchName && matchClass && matchDesc;
    });
  }

  get_translate(id: number): TranslationString {
    // a faire en fonction de la langu selectionner
    if (this.data_store.translationResource.hasValue()) {
      return this.data_store.translationResource.value()[id-1]
    } else {
      return defaultTranslate
    }
  }

  constructor(
    @Inject(MAT_DIALOG_DATA) private data: { filterClass: number },
    private dialogRef: MatDialogRef<selectorComponent>) {
    this.filterClass = data.filterClass;

    if (!this.data_store.modulesResource.hasValue()) { // dont load twice if values are load
      this.data_store.load_modules()
    }
    if (!this.data_store.translationResource.hasValue()) {
      this.data_store.load_translations()
    }
  }

  select(module: ModuleResponse): void {
    this.dialogRef.close(module);
  }
}
