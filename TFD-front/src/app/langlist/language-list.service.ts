import {Injectable, signal} from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class LanguageListService {
  private selected$$ = signal<string>('ko');

  get selected() {
    if (this.selected$$) {
      return this.selected$$();
    }
    return "ko"
  }

  set selected(selectedCode: string) {
    this.selected$$.set(selectedCode);
  }
}
