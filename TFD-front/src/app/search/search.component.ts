import { Component, inject } from '@angular/core';

import { visualStore } from '../store/display.store';
import { getUILabel } from '../lang.utils';

@Component({
  standalone: true,
  selector: 'search-tab',
  imports: [],
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.scss', '../../styles.scss']
})
export class SearchComponent {
  private visualStore = inject(visualStore);

  label(key: Parameters<typeof getUILabel>[1]) {
    return getUILabel(this.visualStore.get_lang(), key);
  }
}
