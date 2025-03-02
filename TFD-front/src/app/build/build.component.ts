import {ChangeDetectorRef, Component, inject, input, InputSignal, OnInit, signal, ViewChild} from '@angular/core';
import {CdkDragDrop, DragDropModule} from '@angular/cdk/drag-drop';
import { Module, defaultModule } from '../module/module.model';
import { CommonModule } from '@angular/common';
import { ModuleService } from '../module/module.service';
import {appStore} from '../store/data.store';
import {ModuleComponent} from '../module/module.component';

@Component({
  imports: [CommonModule, DragDropModule, ModuleComponent],
  selector: 'build',
  templateUrl: './build.component.html',
  styleUrls: ['./build.component.scss', '../app.component.scss']
})
export class BuildComponent implements OnInit {
  readonly store = inject(appStore);

  nbslots: number = 10;
  defaultModules: Module[] = []

  searchTerms$$ = this.store.searchTerms
  selectedModule$$ = signal<Module[]>([defaultModule]);
  language$$ = this.store.language;

  constructor(
    private cdr: ChangeDetectorRef,
    private objectService: ModuleService) {
    for (let i = 0; i < this.nbslots; i++) {
      this.defaultModules.push(defaultModule);
    }
    this.selectedModule$$ = signal<Module[]>(this.defaultModules);
  }

  ngOnInit(): void {}

  public get connectedDropLists(): string[] {
    return this.selectedModule$$().map((_, index) => index.toString());
  }

  onDragStart(event: DragEvent) {
    if (event.dataTransfer) {
      event.dataTransfer.setDragImage(new Image(), 0, 0); // Supprime l'aperçu
    }
  }

  drop(event: CdkDragDrop<Module[]>): void {
    let filteredModules = this.objectService.filteredObjects(
      this.store.modules_availables(),
      this.store.language(),
      this.searchTerms$$())

    const droppedModule = filteredModules[event.previousIndex];

    if (this.fetch_compatibility(droppedModule)) {
      return;
    }

    let toMove = +event.container.id
    let cameFromSelected = !isNaN(Number(event.previousContainer.id));

    if (this.nbslots === 12) {
      let constraint = this.objectService.getContraint(cameFromSelected
        ? this.selectedModule$$()[event.previousIndex]
        : droppedModule)
      console.log(droppedModule, constraint)
      if (constraint === "Sub" && !cameFromSelected) {
        toMove = 1
      } else if (constraint === "Skill" && !cameFromSelected) {
        toMove = 0
      } else if (toMove <= 1 && !cameFromSelected) {
        toMove += 2
        if (Number(event.previousContainer.id) === toMove) {
          return;
        }
      } else if (cameFromSelected) {
        return;
      }
    }

    this.selectedModule$$.update((modules) => {
      const updatedModules = [...modules];
      if (cameFromSelected) {
        updatedModules[toMove] = modules[Number(event.previousContainer.id)]
      } else {
        updatedModules[toMove] = droppedModule;
      }
      return updatedModules;
    });

    if (cameFromSelected) {
      this.reset(+ event.previousContainer.id)
    }
  }

  fetch_compatibility(droppedModule: Module): boolean {
    const selectedModules = this.selectedModule$$();

    let constraint = this.objectService.getContraint(droppedModule)

    for (const mod of selectedModules) {
      const modType = mod.type.split(",");
      const modName = mod.name;
      const modConstraint = modType.length > 1 ? modType[1].trim() : "None";

      console.log(mod)

      if (modName["ko"] === droppedModule.name["ko"]) {
        return true;
      } else if (modConstraint === constraint  && constraint !== "None" && mod.id !== 0) {
        return true;
      }
    }

    return false;
  }

  reset(index: number) {
    this.selectedModule$$.update((modules) => {
      const updatedModules = [...modules];
      updatedModules[index] = defaultModule;
      return updatedModules;
    });
  }
}
