import { Directive, EventEmitter, Input, Output, HostListener } from '@angular/core';

@Directive({
  selector: '[holdAction]',
  standalone: true
})
export class HoldActionDirective {
  @Input() holdDelay = 500;
  @Output() holdActionHold = new EventEmitter<void>();
  @Output() holdActionClick = new EventEmitter<void>();

  private timeoutId: any;
  private isHolding = false;
  private pointerDown = false;

  @HostListener('pointerdown')
  onPointerDown(): void {
    this.isHolding = false;
    this.pointerDown = true;
    clearTimeout(this.timeoutId);
    this.timeoutId = setTimeout(() => {
      if (this.pointerDown) {
        this.isHolding = true;
        this.pointerDown = false;
        this.holdActionHold.emit();
      }
    }, this.holdDelay);
  }

  @HostListener('pointerup')
  onPointerUp(): void {
    clearTimeout(this.timeoutId);
    if (!this.isHolding && this.pointerDown) {
      this.holdActionClick.emit();
    }
    this.pointerDown = false;
  }

  @HostListener('pointerleave')
  onPointerLeave(): void {
    clearTimeout(this.timeoutId);
    this.pointerDown = false;
  }

  @HostListener('pointercancel')
  onPointerCancel(): void {
    clearTimeout(this.timeoutId);
    this.pointerDown = false;
  }
}
