import {Component, ChangeDetectorRef, inject, Input, EventEmitter, Output} from '@angular/core';
import { CommonModule } from '@angular/common';
import { selectorComponent } from '../selector/selector.component';
import { MatDialog } from '@angular/material/dialog';
import { dataStore, defaultTranslate, ModuleResponse, TranslationString } from '../../store/data.store';
import { ModuleComponent } from './display/module-display.component';

@Component({
  standalone: true,
  selector: 'module-build',
  imports: [CommonModule, ModuleComponent],
  templateUrl: './module.component.html',
  styleUrls: ['./module.component.scss', '../main/main.component.scss' ,'../../../styles.scss']
})
export class ModuleBuildComponent {
  readonly data_store = inject(dataStore);
  private _module!: ModuleResponse;
  @Output() moduleSelected = new EventEmitter<ModuleResponse>();

  constructor(
    private dialog: MatDialog,
    private cdr: ChangeDetectorRef) {
  }

  @Input()
  set module(value: ModuleResponse) {
    this._module = value;
    this.cdr.markForCheck();
  }
  get module(): ModuleResponse {
    return this._module;
  }

  openDialog(): void {
    const dialogRef = this.dialog.open(selectorComponent, {
      autoFocus: true,
      data: { //TODO: faire un type
        filterClass: 593
        // ajouter l'id du descendant
      }
    });

    dialogRef.afterClosed().subscribe(res => {
      this._module = res;
      this.moduleSelected.emit(res);
      this.cdr.detectChanges();
    });
  }
}
