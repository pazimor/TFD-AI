import { Component, computed, ElementRef, inject, input, InputSignal, ViewChild } from '@angular/core';
import { DragDropModule } from '@angular/cdk/drag-drop';
import { Module } from './module.model';
import { CommonModule } from '@angular/common';
import { visualStore } from '../store/display.store';

@Component({
  imports: [CommonModule, DragDropModule],
  selector: 'module-item',
  templateUrl: './module.component.html',
  styleUrls: ['./module.component.scss', './modules-tiers.scss']
})

export class ModuleComponent {
  readonly currentModule: InputSignal<Module> = input.required<Module>()
  readonly isSelected: InputSignal<Boolean> = input.required<Boolean>()

  readonly visual_store = inject(visualStore);

  @ViewChild('statsDiv') statsDiv!: ElementRef;

  showTooltip = false;
  language$$ = this.visual_store.language;
  contrainte = computed(() => this.currentModule().type?.split(',')[1]?.trim() ?? "")

  onTooltipEnter(): void {
    this.showTooltip = true;

    setTimeout(() => {
      if (!this.statsDiv) return;

      const tooltipRect = this.statsDiv.nativeElement.getBoundingClientRect();
      const screenWidth = window.innerWidth || document.documentElement.clientWidth;

      if (tooltipRect.right > screenWidth) {
        this.statsDiv.nativeElement.classList.add('flipLeft');
      } else {
        this.statsDiv.nativeElement.classList.remove('flipLeft');
      }
    }, 0);
  }

  onTooltipLeave(): void {
    this.showTooltip = false;
    if (this.statsDiv) {
      this.statsDiv.nativeElement.classList.remove('flipLeft');
    }
  }
}
