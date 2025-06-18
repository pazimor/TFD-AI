import { Component, Input, Output, EventEmitter, inject, computed, Signal, signal } from '@angular/core';
import { buildStore } from '../../../store/build.store';
import { CommonModule, DatePipe } from '@angular/common';
import { MatIconModule } from '@angular/material/icon';
import { Clipboard } from '@angular/cdk/clipboard';
import { environment } from '../../../../env/environment';
import { Router } from '@angular/router';

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
  private buildStore = inject(buildStore)
  @Input({ required: true }) build!: BuildSummary;
  @Output() viewBuild = new EventEmitter<number>();

  protected isSelected: Signal<boolean> = computed(
    () => this.buildStore.currentBuild.build_id() === this.build.build_id);

  constructor(private clipboard: Clipboard) {}


  onSelect() {
    this.viewBuild.emit(this.build.build_id);
  }
  copyBuild() {
    this.clipboard.copy(environment.copyLink + "build-maker?build=" + this.build.build_id);
  }

  unlinkgBuild() {
    this.buildStore.setBuildID(0);
    this.viewBuild.emit(0);
  }
}
