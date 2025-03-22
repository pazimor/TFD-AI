import {
  Component, computed,
  inject, input, InputSignal,
  OnInit,
  Signal
} from '@angular/core';
import { CommonModule } from '@angular/common';
import { CdkDragDrop, DragDropModule } from '@angular/cdk/drag-drop';
import { Module} from '../module/module.model'
import { FormsModule } from '@angular/forms';
import { dataStore } from '../store/data.store';
import { BuildComponent } from '../build/build.component';
import { ModuleService } from '../module/module.service';
import { ModuleComponent } from '../module/module.component';
import {Selector, visualStore} from '../store/display.store';
import {skip} from 'rxjs';


@Component({
  imports: [CommonModule, DragDropModule, FormsModule, ModuleComponent],
  providers: [BuildComponent],
  selector: 'module-bank',
  templateUrl: './module-bank.component.html',
  styleUrls: ['./module-bank.component.scss']
})
export class ModuleBankComponent implements OnInit {

  readonly data_store = inject(dataStore);
  readonly visual_store = inject(visualStore);



  searchTerm: string = "";
  availableModules$$: Signal<Module[]> = this.data_store.modules_available
  displayonly$$: Signal<string> = this.visual_store.displayOnly;


  ngOnInit(): void {}

  constructor(
    private moduleService: ModuleService,
    private buildComponent: BuildComponent
  ) {}

  public get connectedDropLists(): string[] {
    const values: string[] = [];
    for (let prefix in Selector) {
      if (prefix === "DEFAULT") {

      } else if (prefix === Selector.CHARACTERE) {
        for (let i = 0; i < 12; i++) {
          values.push(`${prefix}_${i}`);
        }
      } else {
        for (let i = 0; i < 10; i++) {
          values.push(`${prefix}_${i}`);
        }
      }
    }
    return values;
  }

  onSearchTermChange(newValue: any) {
    if (newValue.inputType === 'deleteContentBackward') {
      this.searchTerm = this.searchTerm.slice(0, -1);
    } else if (newValue.inputType === 'insertText') {
      this.searchTerm += newValue.data
    }

    this.visual_store.set_search(this.searchTerm)
  }

  viewModules() {
    return computed(() => this.moduleService.filteredObjects(
      this.availableModules$$(),
      this.visual_store.language(),
      this.visual_store.searchTerms(),
      this.displayonly$$()
    ))()

  }

  drop(event: CdkDragDrop<Module[]>) {
    this.buildComponent.reset(+ event.previousContainer.id)
  }
}
