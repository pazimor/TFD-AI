import {
  Component,
  ElementRef, inject,
  OnInit,
  QueryList, Signal,
  signal,
  ViewChild,
} from '@angular/core';
import { CommonModule } from '@angular/common';
import { CdkDragDrop, DragDropModule } from '@angular/cdk/drag-drop';
import { Module} from '../module/module.model'
import { FormsModule } from '@angular/forms';
import { appStore } from '../store/data.store';
import { BuildComponent } from '../build/build.component';
import { ModuleService } from '../module/module.service';
import { ModuleComponent } from '../module/module.component';


@Component({
  imports: [CommonModule, DragDropModule, FormsModule, ModuleComponent],
  providers: [BuildComponent],
  selector: 'module-bank',
  templateUrl: './module-bank.component.html',
  styleUrls: ['./module-bank.component.scss', '../module/modules-tiers.scss']
})
export class ModuleBankComponent implements OnInit {

  readonly store = inject(appStore);

  searchTerm: string = "";
  availableModules$$: Signal<Module[]> = this.store.modules_availables

  ngOnInit(): void {}

  constructor(
    private moduleService: ModuleService,
    private buildComponent: BuildComponent
  ) {}

  onSearchTermChange(newValue: any) {
    if (newValue.inputType === 'deleteContentBackward') {
      this.searchTerm = this.searchTerm.slice(0, -1); //
    } else if (newValue.inputType === 'insertText') {
      this.searchTerm += newValue.data
    }

    this.store.set_Search(this.searchTerm)
  }

  viewModules() {
    return this.moduleService.filteredObjects(
      this.availableModules$$(),
      this.store.language(),
      this.store.searchTerms()
    )
  }

  drop(event: CdkDragDrop<Module[]>) {
    this.buildComponent.reset(+ event.previousContainer.id)
  }
}
