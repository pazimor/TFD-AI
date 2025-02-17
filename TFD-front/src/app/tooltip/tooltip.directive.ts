import { Directive, HostListener } from '@angular/core';
import { TooltipService } from './tooltip.service';

@Directive({
  selector: '[appTooltip]'
})
export class TooltipDirective {
  constructor(private tooltipService: TooltipService) {}

  @HostListener('mouseenter', ['$event'])
  onMouseEnter(event: MouseEvent) {
    this.tooltipService.showTooltip(event);
  }

  @HostListener('mousemove', ['$event'])
  onMouseMove(event: MouseEvent) {
    this.tooltipService.updateTooltipPosition(event);
  }

  @HostListener('mouseleave')
  onMouseLeave() {
    this.tooltipService.hideTooltip();
  }

  // Masquer le tooltip dès que l'utilisateur clique sur l'élément
  @HostListener('mousedown', ['$event'])
  onMouseDown(event: MouseEvent) {
    this.tooltipService.hideTooltip();
  }

  // En complément, cacher aussi lors du début du drag
  @HostListener('dragstart', ['$event'])
  onDragStart(event: DragEvent) {
    this.tooltipService.hideTooltip();
  }
}
