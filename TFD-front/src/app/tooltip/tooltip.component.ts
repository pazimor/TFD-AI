import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';


@Component({
  standalone: true,
  selector: 'app-tooltip',
  imports: [CommonModule],
  template: `<div class="tooltip-debug"></div>`,
  styles: [`
    .tooltip-debug {
      width: 100px;
      height: 100px;
      background-color: red;
      position: absolute;
      z-index: 1000;
    }
  `]
})

export class Tooltip {}
