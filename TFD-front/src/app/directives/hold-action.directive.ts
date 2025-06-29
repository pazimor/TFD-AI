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

  @HostListener('pointerdown')
  onPointerDown(): void {
    this.isHolding = false;
    clearTimeout(this.timeoutId);
    this.timeoutId = setTimeout(() => {
      this.isHolding = true;
      this.holdActionHold.emit();
    }, this.holdDelay);
  }

  @HostListener('pointerup')
  @HostListener('pointerleave')
  @HostListener('pointercancel')
  onPointerUp(): void {
    clearTimeout(this.timeoutId);
    if (!this.isHolding) {
      this.holdActionClick.emit();
    }
  }
}
