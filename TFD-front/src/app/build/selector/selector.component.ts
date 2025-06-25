import {Component, Inject, inject, Input} from '@angular/core';

import {dataStore, defaultTranslate, TranslationString} from '../../store/data.store';
import { visualStore } from '../../store/display.store';
import { getTranslationField, getUILabel } from '../../lang.utils';
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
    ModuleComponent,
    MatDialogModule,
    MatProgressSpinnerModule,
    FormsModule,
    DescendantDisplayComponent,
    WeaponDisplayComponent,
    ReactorDisplayComponent,
    ExternalDisplayComponent
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
  selectedReactorGroup: Reactor[] | null = null;

  selectedReactorKey: string | undefined = undefined;

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

  filteredReactorsbynameid() {
    const reactors = this.data_store.reactorResource.value() ?? []
    return reactors.filter(reactor => {
      const key = this.selectedReactorKey?.split("-") ?? ["0", "Tier1"]
      return (reactor.reactor_name_id === +key[0] && reactor.reactor_tier_id === key[1])
    })
  }

  filteredReactors() {
    const reactors = this.data_store.reactorResource.value() ?? [];
    const seen = new Set<string>();
    return reactors.filter(r => {
      const key = `${r.reactor_name_id}_${r.reactor_tier_id ?? ''}`;
      if (seen.has(key)) { return false; }
      seen.add(key);
      return true;
    });

  }

  reactorGroups() {
    const list = this.data_store.reactorResource.value() ?? [];
    const groups: Record<string, Reactor[]> = {};
    for (const r of list) {
      const key = r.image_url ?? '';
      if (!groups[key]) {
        groups[key] = [];
      }
      groups[key].push(r);
    }
    return Object.values(groups);
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
    // resources are preloaded in main component
  }

  label(key: Parameters<typeof getUILabel>[1]) {
    return getUILabel(this.visual_store.get_lang(), key);
  }

  selectModules(module: ModuleResponse): void {
    this.dialogRef.close(module.module_id);
  }

  selectDescendant(descendant: DescendantsResponse): void {
    this.dialogRef.close(descendant.descendant_id);
  }

  selectWeapon(weapon: WeaponResponse): void {
    this.dialogRef.close(weapon.weapon_id);
  }

  selectReactor(reactor: Reactor): void {
    console.log(reactor);
    this.dialogRef.close(reactor.reactor_id);
  }

  selectReactorGroup(reactor: Reactor): void {
    this.selectedReactorKey = reactor.reactor_name_id + '-' + reactor.reactor_tier_id;
  }

  backToGroups(): void {
    this.selectedReactorKey = undefined;
  }

  selectExternal(external: ExternalComponent): void {
    this.dialogRef.close(external.external_component_id);
  }

  name(id: number): string {
    const langKey = getTranslationField(this.visual_store.get_lang());
    const translation = this.get_translate(id);
    // Guard against missing translation object or key
    const value = (translation as any)?.[langKey];
    return value ?? '';
  }
}
