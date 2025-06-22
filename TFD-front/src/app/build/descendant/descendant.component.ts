import { Component, inject, effect } from '@angular/core';

import { ModuleBuildComponent } from '../module/module.component';
import { ReactorBuildComponent } from '../reactor/reactor.component';
import { ExternalBuildComponent } from '../external/external.component';
import { dataStore } from '../../store/data.store';
import { selectorData } from '../../types/selector.types';
import { DescendantDisplayComponent } from './display/descendant-display.component';
import { ModuleResponse } from '../../types/module.types';
import { defaultDescendants, DescendantsResponse, unsetDescendants } from '../../types/descendant.types';
import { selectorComponent } from '../selector/selector.component';
import { MatDialog } from '@angular/material/dialog';
import { ArcheronTreeComponent } from './tree/archeron-tree.component';
import { buildStore } from '../../store/build.store';

@Component({
  standalone: true,
  selector: 'descendant-build',
  imports: [
    ModuleBuildComponent,
    DescendantDisplayComponent,
    ReactorBuildComponent,
    ExternalBuildComponent
],
  templateUrl: './descendant.component.html',
  styleUrls: ['./descendant.component.scss', '../main/main.component.scss' ,'../../../styles.scss']
})
export class DescedantBuildComponent {
  readonly data_store = inject(dataStore);
  readonly build_store = inject(buildStore);

  readonly _syncEffect = effect(() => {
    this.module_data.descendant = this.build_store.descendant().descendant_id;
  });

  module_data: selectorData = {
    selectitems: "modules",
    filterClass: 593,
    descendant: undefined
  }

  descendant_data: selectorData = {
    selectitems: "descendants",
    filterClass: 593,
    descendant: undefined
  }

  descendant = this.build_store.descendant;
  modules = this.build_store.descendantModules;
  reactor = this.build_store.reactor;
  externals = this.build_store.externals;

  handleModuleSelected(index: number, module: ModuleResponse) {
    const currentModules = this.modules();
    const isDuplicate = currentModules.some((m, i) => i !== index && m?.module_id === module.module_id);
    const isDuplicateType = module.module_type !== 1 &&
      currentModules.some((m, i) => i !== index && m?.module_type === module.module_type);
    const forcedIndex = module.available_module_slot_type_id === "892" ? 6 :
      module.available_module_slot_type_id === "901" ? 0 :
        index;
    if (module.id === 0) {
      return;
    }

    if (isDuplicate || isDuplicateType || forcedIndex !== index) {
      this.build_store.updateDescendantModule(index, { ...currentModules[index] });
      if (forcedIndex === index) {
        return;
      }
    }

    this.build_store.updateDescendantModule(forcedIndex, module);
  }

  constructor(private dialog: MatDialog) {}

  openSkillTreeDialog(): void {
    this.data_store.load_boards();
    this.dialog.open(ArcheronTreeComponent, {
      autoFocus: true,
      data: this.build_store.descendant(),
      width: '600px',
    });
  }

  openDialog(): void {

    const dialogRef = this.dialog.open(selectorComponent, {
      autoFocus: true,
      data: this.descendant_data
    });

    dialogRef.afterClosed().subscribe((id: number) => {
      if (id === undefined) {
        id = 0;
      }

      const res = this.data_store.descendantResource.value()
        ?.filter(des => des.descendant_id === id)[0]
        ?? unsetDescendants
      this.build_store.setDescendant(res);
      this.module_data.descendant = res.descendant_id

      //TODO: double check compatibles modules
    });
  }

}
