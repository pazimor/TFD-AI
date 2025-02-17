import {
  Component,
  ElementRef,
  OnInit,
  QueryList,
  signal,
  ViewChild,
} from '@angular/core';
import { CommonModule } from '@angular/common';
import { CdkDragDrop, DragDropModule } from '@angular/cdk/drag-drop';
import { ModuleService } from './module/module.service'
import { Module, defaultModule} from './module/module.model'
import { FormsModule } from '@angular/forms';
import { BuildComponent } from './build/build.component';
import { TooltipDirective } from './tooltip/tooltip.directive';
import {LanguageListComponent} from './langlist/language-list.component';


@Component({
  standalone: true,
  imports: [CommonModule, DragDropModule, FormsModule, BuildComponent, TooltipDirective, LanguageListComponent],
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss', './scss/modules-tiers.scss']
})
export class AppComponent implements OnInit {
  @ViewChild(BuildComponent) buildComponent!: BuildComponent;
  @ViewChild(TooltipDirective) tooltipDirective!: TooltipDirective;
  @ViewChild(LanguageListComponent) languageListComponent!: LanguageListComponent;

  title = 'TFD-front';

  availableObjects$$ = signal<Module[]>([]);
  searchTerm: string = '';

  constructor(
    private objectService: ModuleService) {}

  ngOnInit(): void {
    this.objectService.getObjects().subscribe(objects => {
      this.availableObjects$$.set(objects);
    });
  }

  getFilteredObjects(): Module[] {
    if (this.languageListComponent) {
      return this.objectService.filteredObjects(
        this.availableObjects$$(),
        this.languageListComponent.selected$$(),
        this.searchTerm);
    }
    return [defaultModule]
  }

  drop(event: CdkDragDrop<Module[]>) {
      this.buildComponent.reset()
  }
}
