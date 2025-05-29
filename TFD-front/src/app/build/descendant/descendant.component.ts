import { Component, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ModuleBuildComponent } from '../module/module.component';
import {defaultModule, ModuleResponse} from '../../store/data.store';

@Component({
  standalone: true,
  selector: 'descendant-build',
  imports: [CommonModule, ModuleBuildComponent],
  templateUrl: './descendant.component.html',
  styleUrls: ['./descendant.component.scss', '../main/main.component.scss' ,'../../../styles.scss']
})
export class DescedantBuildComponent {

  modules = signal<(ModuleResponse)[]>(
    Array.from({ length: 12 }, () => ({ ...defaultModule }))
  );

  handleModuleSelected(index: number, module: ModuleResponse) {
    const currentModules = this.modules();

    const isDuplicate = currentModules.some((m, i) => i !== index && m?.module_id === module.module_id);

    const isDuplicateType = module.module_type !== 1 &&
      currentModules.some((m, i) => i !== index && m?.module_type === module.module_type);

    const forcedIndex = module.available_module_slot_type_id === "892" ? 6 :
      module.available_module_slot_type_id === "901" ? 0 :
        index;

    if (isDuplicate || isDuplicateType || forcedIndex !== index) {
      this.modules.update(current => {
        const copy = [...current];
        copy[index] = { ...copy[index] };
        return copy;
      });
      if (forcedIndex === index) {
        return;
      }
    }

    this.modules.update(current => {
      const copy = [...current];
      copy[forcedIndex] = module;
      return copy;
    });
  }

  constructor() {}
}
