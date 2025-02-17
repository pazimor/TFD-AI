import {AfterViewInit, Component, signal} from '@angular/core';
import { CommonModule } from '@angular/common';
import { Module } from '../module/module.model';

@Component({
  standalone: true,
  imports: [CommonModule],
  selector: 'app-language-list',
  templateUrl: './language-list.component.html',
  styleUrls: ['./language-list.component.scss']
})
export class LanguageListComponent implements AfterViewInit {

  selected$$ = signal<string>('fr');
  isLanguageListReady = false;

  ngAfterViewInit(): void {
    // On utilise setTimeout pour forcer la détection de changement après l'initialisation
    setTimeout(() => {
      this.isLanguageListReady = true;
    });
  }

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
    return obj.name[this.selected$$()]
  }

  onLanguageChange(selectedCode: string): void {
    this.selected$$.set(selectedCode)
  }
}
