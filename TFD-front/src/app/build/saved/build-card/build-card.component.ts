import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule, DatePipe } from '@angular/common';
import { MatIconModule } from '@angular/material/icon';
import { Clipboard } from '@angular/cdk/clipboard';

export interface BuildSummary { // Exporting for potential use in parent
  build_id: number;
  build_name: string;
  updated_at?: string;
  user_google_id?: string; // For potential future use on card
  // build_data might be too large for summary, but could have a snippet
}

@Component({
  selector: 'app-build-card',
  imports: [CommonModule, DatePipe, MatIconModule],
  templateUrl: './build-card.component.html',
  styleUrls: ['./build-card.component.scss']
})
export class BuildCardComponent {
  @Input({ required: true }) build!: BuildSummary;
  @Output() viewBuild = new EventEmitter<number>();

  constructor(private clipboard: Clipboard) {}

  onCardClick(): void {
    this.viewBuild.emit(this.build.build_id);
  }

  copyBuild() {
    this.clipboard.copy("http://localhost:4200/build-maker?build=" + this.build.build_id);
  }
}
