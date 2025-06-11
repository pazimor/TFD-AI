import {Component, Inject, inject, Input} from '@angular/core';
import { CommonModule } from '@angular/common';
import {dataStore, defaultTranslate, TranslationString} from '../../store/data.store';
import { visualStore } from '../../store/display.store';
import { getTranslationField } from '../../lang.utils';
import { ModuleComponent } from '../module/display/module-display.component';
import { ReactorDisplayComponent } from '../reactor/display/reactor-display.component';
import { ExternalDisplayComponent } from '../external/display/external-display.component';
import {MAT_DIALOG_DATA, MatDialogModule, MatDialogRef} from '@angular/material/dialog';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { FormsModule } from '@angular/forms';
import {selectorData} from '../../types/selector.types';
import {ModuleResponse} from '../../types/module.types';
import { DescendantDisplayComponent } from '../descendant/display/descendant-display.component';
import { DescendantsResponse } from '../../types/descendant.types';
import { WeaponDisplayComponent } from '../weapon/display/weapon-display.component';
import { WeaponResponse } from '../../types/weapon.types';
import { Reactor } from '../../types/reactor.types';
import { ExternalComponent } from '../../types/external.types';

@Component({
  standalone: true,
  selector: 'selector',
  imports: [
    CommonModule,
    ModuleComponent,
    MatDialogModule,
    MatProgressSpinnerModule,
    FormsModule,
    DescendantDisplayComponent,
    WeaponDisplayComponent,
    ReactorDisplayComponent,
    ExternalDisplayComponent,
  ],
  templateUrl: './selector.component.html',
  styleUrls: ['./selector.component.scss', '../../../styles.scss']
})
export class selectorComponent {
  readonly data_store = inject(dataStore);
  readonly visual_store = inject(visualStore);

  filterClass: number;
  type: string = "";

  searchText = '';
  requireDescendant = false;

  compareDescendantIDs(module: ModuleResponse): boolean {
    const ids = (module.available_descendant_id ?? '')
      .split(',')
      .map(id => id.trim())
      .filter(id => id !== '');

    if (!this.data.descendant || ids[0] === undefined) {
      return true;
    }

    const targetId =
      typeof this.data.descendant === 'object'
        ? (this.data.descendant as any).id ?? ''
        : String(this.data.descendant);

    return ids.includes(String(targetId));
  }

  filteredModules() {
    return this.data_store.modulesResource.value()?.filter(module => {
      const langKey = getTranslationField(this.visual_store.get_lang());
      const name = (this.get_translate(module.module_name_id) as any)[langKey] as string;
      const matchName = !this.searchText || name?.toLowerCase().includes(this.searchText.toLowerCase());
      const matchClass = !this.filterClass || (module.module_class_id === this.filterClass);
      const matchDesc = this.compareDescendantIDs(module);
      return matchName && matchClass && matchDesc;
    });
  }

  filteredDescendants() {
    return this.data_store.descendantResource.value()
  }

  filteredWeapons() {
    return this.data_store.weaponResource.value()
  }

  filteredReactors() {
    return this.data_store.reactorResource.value()
  }

  filteredExternals() {
    return this.data_store.externalResource.value()
  }

  get_translate(id: number): TranslationString {
    if (this.data_store.translationResource.hasValue()) {
      return this.data_store.translationResource.value()[id-1]
    } else {
      return defaultTranslate
    }
  }

  constructor(
    @Inject(MAT_DIALOG_DATA) private data: selectorData,
    private dialogRef: MatDialogRef<selectorComponent>) {
    this.filterClass = data.filterClass ?? 0;
    this.type = data.selectitems;
    // dont load twice if values are load
    if (!this.data_store.modulesResource.hasValue()) {
      this.data_store.load_modules()
    }
    if (!this.data_store.translationResource.hasValue()) {
      this.data_store.load_translations()
    }
    if (!this.data_store.descendantResource.hasValue()) {
      this.data_store.load_descendants()
    }
    if (!this.data_store.weaponResource.hasValue()) {
      this.data_store.load_weapons()
    }
    if (!this.data_store.reactorResource.hasValue()) {
      this.data_store.load_reactors()
    }
    if (!this.data_store.externalResource.hasValue()) {
      this.data_store.load_externals()
    }
  }

  selectModules(module: ModuleResponse): void {
    this.dialogRef.close(module);
  }

  selectDescendant(descendant: DescendantsResponse): void {
    this.dialogRef.close(descendant);
  }

  selectWeapon(weapon: WeaponResponse ): void {
    this.dialogRef.close(weapon);
  }

  selectReactor(reactor: Reactor): void {
    this.dialogRef.close(reactor);
  }

  selectExternal(external: ExternalComponent): void {
    this.dialogRef.close(external);
  }
}
