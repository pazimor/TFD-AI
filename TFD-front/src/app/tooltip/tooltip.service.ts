import { Injectable } from '@angular/core';
import { Overlay, OverlayRef, GlobalPositionStrategy } from '@angular/cdk/overlay';
import { ComponentPortal } from '@angular/cdk/portal';
import { Tooltip } from './tooltip.component';

@Injectable({ providedIn: 'root' })
export class TooltipService {
  private overlayRef!: OverlayRef;
  private positionStrategy!: GlobalPositionStrategy;
  private offset: number = 10;
  private tooltipWidth: number = 100; // largeur du tooltip (à adapter si besoin)

  constructor(private overlay: Overlay) {}

  public showTooltip(event: MouseEvent) {
    this.positionStrategy = this.overlay.position().global();
    // Calcul de la position horizontale :
    // Si le tooltip déborde à droite, on le place à gauche du curseur.
    const leftPos = (event.clientX + this.offset + this.tooltipWidth > window.innerWidth)
      ? event.clientX - this.tooltipWidth - this.offset
      : event.clientX + this.offset;

    this.positionStrategy.left(leftPos + 'px');
    this.positionStrategy.top(event.clientY + this.offset + 'px');

    this.overlayRef = this.overlay.create({
      positionStrategy: this.positionStrategy,
      hasBackdrop: false,
      panelClass: 'custom-tooltip-panel'
    });

    const tooltipPortal = new ComponentPortal(Tooltip);
    this.overlayRef.attach(tooltipPortal);
  }

  public updateTooltipPosition(event: MouseEvent) {
    if (this.overlayRef) {
      const leftPos = (event.clientX + this.offset + this.tooltipWidth > window.innerWidth)
        ? event.clientX - this.tooltipWidth - this.offset
        : event.clientX + this.offset;
      this.positionStrategy.left(leftPos + 'px');
      this.positionStrategy.top(event.clientY + this.offset + 'px');
      this.overlayRef.updatePosition();
    }
  }

  public hideTooltip() {
    if (this.overlayRef) {
      this.overlayRef.detach();
    }
  }
}
