import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CdkDragDrop, DragDropModule, moveItemInArray, transferArrayItem } from '@angular/cdk/drag-drop';
import { ModuleService } from './module/module.service'
import { Module } from './module/module.model'
import { FormsModule } from '@angular/forms';
import {BehaviorSubject, map, Observable, tap} from 'rxjs';


@Component({
  standalone: true,
  imports: [CommonModule, DragDropModule, FormsModule],
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  title = 'TFD-front';

  defaultModule: Module = {
    id: 0,
    name: "",
    type: "",
    statistiques: "",
    optional_statistiques: "",
    stack_id: "",
    stack_description: "",
    display_data: {
      img: "",
      tier: "",
    },
    drag: true
  }
  availableObjects$: BehaviorSubject<Module[]> = new BehaviorSubject<Module[]>([]);
  selectedObjects$: BehaviorSubject<Module[]> = new BehaviorSubject<Module[]>([this.defaultModule]);

  availableObjects: Module[] = [];
  selectedObjects: Module[] = [];

  searchTerm: string = '';

  constructor(private objectService: ModuleService) {}

  ngOnInit(): void {
    this.objectService.getObjects().subscribe(objects => {
      this.availableObjects = objects;
      this.availableObjects$.next(objects);
    });

    this.selectedObjects$.subscribe(objects => {
      this.selectedObjects = objects;
    });
  }

  filteredObjects(): Observable<Module[]> {
    return this.availableObjects$.pipe(
      map(objects =>
        objects.filter(obj => obj.name.toLowerCase().includes(this.searchTerm.toLowerCase()))
      )
    );
  }

  drop(event: CdkDragDrop<Module[]>) {

    let available = this.availableObjects$.getValue();
    let selected = [...this.selectedObjects$.getValue()];

    this.filteredObjects().subscribe(filteredModules => {
      const droppedModule = filteredModules[event.previousIndex];

      if (event.container.id === 'selectedList' && event.previousContainer.id === 'availableList') {
        selected = [droppedModule];

      } else if (event.container.id === 'availableList' && event.previousContainer.id === 'selectedList') {
        selected = [this.defaultModule];
      }
    });

    this.selectedObjects$.next(selected);
    this.availableObjects$.next(available);
  }
}
