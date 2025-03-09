import {
  ChangeDetectorRef,
  Component,
  computed,
  inject,
  input,
  InputSignal,
  OnInit, Signal,
  signal,
  ViewChild
} from '@angular/core';
import {CdkDragDrop, DragDropModule} from '@angular/cdk/drag-drop';
import { Module, defaultModule } from '../module/module.model';
import { CommonModule } from '@angular/common';
import { ModuleService } from '../module/module.service';
import {appStore} from '../store/data.store';
import {ModuleComponent} from '../module/module.component';
import {Character} from '../character/character.model';

@Component({
  imports: [CommonModule, DragDropModule, ModuleComponent],
  selector: 'build',
  templateUrl: './build.component.html',
  styleUrls: ['./build.component.scss', '../app.component.scss']
})
export class BuildComponent implements OnInit {
  readonly store = inject(appStore);

  readonly isDescendantBuild: InputSignal<boolean> = input.required<boolean>();

  defaultModules: Module[] = []
  searchTerms$$ = this.store.searchTerms;
  slots = signal<number>(10);
  selectedModule$$ = signal<Module[]>([defaultModule]);
  language$$ = this.store.language;

  constructor(
    private cdr: ChangeDetectorRef,
    private objectService: ModuleService) {

    this.selectedModule$$ = signal<Module[]>(this.defaultModules);
  }

  ngOnInit(): void {
    this.slots.set(this.isDescendantBuild() ? 12 : 10);

    for (let i = 0; i < this.slots(); i++) {
      this.defaultModules.push(defaultModule);
    }
  }

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
    const constraint = this.objectService.getContraint(cameFromSelected
      ? this.selectedModule$$()[+event.previousContainer.id]
      : droppedModule)


    if (this.slots() === 12) {
      if (constraint === "Sub") {
        toMove = 1
      } else if (constraint === "Skill") {
        toMove = 0
      } else if (toMove <= 1 && !cameFromSelected) {
        toMove += 2
        if (Number(event.previousContainer.id) === toMove) {
          return;
        }
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

    if (cameFromSelected && constraint !== "Sub" && constraint !== "Skill") {
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
