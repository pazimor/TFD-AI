import { AfterViewInit, Component, inject, Signal, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Module } from '../module/module.model';
import { visualStore } from '../store/display.store';

@Component({
  imports: [CommonModule],
  selector: 'language-list',
  templateUrl: './language-list.component.html',
  styleUrls: ['./language-list.component.scss']
})
export class LanguageListComponent {
  readonly store = inject(visualStore);

  // Liste des langues supportées
  languages = [
    { code: 'ko', label: '한국어' },
    { code: 'en', label: 'English' },
    { code: 'de', label: 'Deutsch' },
    { code: 'ja', label: '日本語' },
    { code: 'fr', label: 'Français' },
    { code: 'zh-CN', label: '简体中文' },
    { code: 'zh-TW', label: '繁體中文' },
    { code: 'it', label: 'Italiano' },
    { code: 'pl', label: 'Polski' },
    { code: 'pt', label: 'Português' },
    { code: 'ru', label: 'Русский' },
    { code: 'es', label: 'Español' }
  ];

  getstring(obj: Module): string {
    return obj.name[this.store.language()]
  }

  onLanguageChange(selectedCode: string): void {
    this.store.set_lang(selectedCode)
  }
}
