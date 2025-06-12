import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  standalone: true,
  selector: 'search-tab',
  imports: [CommonModule],
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.scss', '../../styles.scss']
})
export class SearchComponent {}
