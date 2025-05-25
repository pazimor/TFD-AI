import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { selectorComponent } from '../selector/selector.component';
import { MatDialog } from '@angular/material/dialog';

@Component({
  standalone: true,
  selector: 'module-build',
  imports: [CommonModule],
  templateUrl: './module.component.html',
  styleUrls: ['./module.component.scss', '../main/main.component.scss' ,'../../../styles.scss']
})
export class ModuleBuildComponent {
  constructor(private dialog: MatDialog) {}

  openDialog(): void {
    this.dialog.open(selectorComponent, {
      autoFocus: true
    });
  }
}
