import { Directive, EventEmitter, HostListener, Output } from '@angular/core';

@Directive({
  selector: '[appSwipeTabs]',
  standalone: true
})
export class SwipeTabsDirective {
  private startX = 0;
  private startY = 0;
  private readonly threshold = 40;

  @Output() swipeLeft = new EventEmitter<void>();
  @Output() swipeRight = new EventEmitter<void>();

  @HostListener('touchstart', ['$event'])
  onTouchStart(event: TouchEvent) {
    const touch = event.changedTouches[0];
    this.startX = touch.screenX;
    this.startY = touch.screenY;
  }

  @HostListener('touchend', ['$event'])
  onTouchEnd(event: TouchEvent) {
    const touch = event.changedTouches[0];
    const deltaX = touch.screenX - this.startX;
    const deltaY = touch.screenY - this.startY;
    if (Math.abs(deltaX) > Math.abs(deltaY) && Math.abs(deltaX) > this.threshold) {
      if (deltaX < 0) {
        this.swipeLeft.emit();
      } else {
        this.swipeRight.emit();
      }
    }
  }
}
