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
import { ModuleService } from './module/module.service'
import { Module} from './module/module.model'
import { FormsModule } from '@angular/forms';
import { BuildComponent } from './build/build.component';
import { LanguageListComponent } from './langlist/language-list.component';
import { appStore } from './store/data.store';
import {ModuleComponent} from './module/module.component';


@Component({
  imports: [CommonModule, DragDropModule, FormsModule, BuildComponent, LanguageListComponent, ModuleComponent],
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss', './module/modules-tiers.scss']
})
export class AppComponent implements OnInit {
  @ViewChild(BuildComponent) buildComponent!: BuildComponent;
  @ViewChild(LanguageListComponent) languageListComponent!: LanguageListComponent;

  readonly store = inject(appStore);
  title = 'TFD-front';

  searchTerm: string = '';
  availableModules$$: Signal<Module[]> = this.store.modules_availables

  ngOnInit(): void {
  }

  constructor(
    private moduleService: ModuleService
  ) {

  }

  viewModules() {
    let item = this.moduleService.filteredObjects(
      this.availableModules$$(),
      this.store.language(),
      this.searchTerm
    )
    return item
  }

  drop(event: CdkDragDrop<Module[]>) {
      //this.buildComponent.reset()
  }
}
