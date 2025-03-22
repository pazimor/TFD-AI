import { Component, inject,
  input, InputSignal, signal, OnInit
} from '@angular/core';
import { CdkDragDrop, DragDropModule } from '@angular/cdk/drag-drop';
import { defaultModule, Module } from '../module/module.model';
import { CommonModule } from '@angular/common';
import { ModuleService } from '../module/module.service';
import { dataStore } from '../store/data.store';
import { ModuleComponent } from '../module/module.component';
import {Selector, visualStore} from '../store/display.store';

@Component({
  imports: [CommonModule, DragDropModule, ModuleComponent],
  selector: 'build',
  templateUrl: './build.component.html',
  styleUrls: ['./build.component.scss', '../app.component.scss']
})
export class BuildComponent implements OnInit {
  readonly data_store = inject(dataStore);
  readonly visual_store = inject(visualStore);

  readonly selectedBuildNumber: InputSignal<number> = input.required<number>();

  component_name = ""
  selectedModule$$= signal<Module[]>([]);
  searchTerms$$ = this.visual_store.searchTerms;
  language$$ = this.visual_store.language;

  slots = 0

  constructor(private objectService: ModuleService) {}

  ngOnInit() {
    if (this.selectedBuildNumber() == 0) {
      const item = this.data_store.selected_descendant()
      this.selectedModule$$.set(item.modules);
      this.component_name = Selector.CHARACTERE + "_";
    } else if (this.selectedBuildNumber() == 1) {
      const item = this.data_store.selected_weapon_1()
      this.selectedModule$$.set(item.modules)
      this.component_name = Selector.WEAPON1 + "_";
    } else if (this.selectedBuildNumber() == 2) {
      const item = this.data_store.selected_weapon_2()
      this.selectedModule$$.set(item.modules)
      this.component_name = Selector.WEAPON2 + "_";
    } else if (this.selectedBuildNumber() == 3) {
      const item = this.data_store.selected_weapon_3()
      this.selectedModule$$.set(item.modules)
      this.component_name = Selector.WEAPON3 + "_";
    }
    this.slots = this.selectedBuildNumber() === 0 ? 12 : 10;
  }

  public get connectedDropLists(): string[] {
    return this.selectedModule$$().map((_, index) => this.component_name + index.toString());
  }

  onDragStart(event: DragEvent) {
    if (event.dataTransfer) {
      event.dataTransfer.setDragImage(new Image(), 0, 0); // Supprime l'aperçu
    }
  }

  drop(event: CdkDragDrop<Module[]>): void {
    let filteredModules = this.objectService.filteredObjects(
      this.data_store.modules_available(),
      this.visual_store.language(),
      this.searchTerms$$(),
      this.visual_store.displayOnly()
    );

    const droppedModule = filteredModules[event.previousIndex];

    if (this.fetch_compatibility(droppedModule)) {
      return;
    }

    let toMove = +event.container.id.replace(this.component_name, "");
    let moveFrom = +event.previousContainer.id.replace(this.component_name, "");
    let cameFromSelected = !isNaN(moveFrom);
    const constraint = this.objectService.getContraint(
      cameFromSelected ? this.selectedModule$$()[moveFrom] : droppedModule
    );

    if (this.slots === 12) {
      if (constraint === "Sub") {
        toMove = 1;
      } else if (constraint === "Skill") {
        toMove = 0;
      } else if (toMove <= 1 && !cameFromSelected) {
        toMove += 2;
        if (moveFrom === toMove) {
          return;
        }
      }
    }

    const updatedModules = [ ...this.selectedModule$$() ];

    if (cameFromSelected) {
      updatedModules[toMove] = this.selectedModule$$()[moveFrom];
    } else {
      updatedModules[toMove] = droppedModule;
    }

    this.selectedModule$$.set(updatedModules);
    this.data_store.set_build(this.selectedBuildNumber(), updatedModules);

    if (cameFromSelected && constraint !== "Sub" && constraint !== "Skill") {
      this.reset(moveFrom);
    }
  }

  fetch_compatibility(droppedModule: Module): boolean {
    const selectedModules = this.selectedModule$$();

    let constraint = this.objectService.getContraint(droppedModule)

    for (const mod of selectedModules) {
      const modType = mod.type.split(",");
      const modName = mod.name;
      const modConstraint = modType.length > 1 ? modType[1].trim() : "None";

      if (modName["ko"] === droppedModule.name["ko"]) {
        return true;
      } else if (modConstraint === constraint  && constraint !== "None" && mod.id !== 0) {
        return true;
      }
    }

    return false;
  }

  reset(index: number) {
    const updatedModules = [ ...this.selectedModule$$() ]; // nouvelle référence
    updatedModules[index] = defaultModule;
    this.selectedModule$$.set(updatedModules);
    this.data_store.set_build(this.selectedBuildNumber(), updatedModules);
  }
}
