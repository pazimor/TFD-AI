import { AfterViewInit, Component, inject, OnInit, Signal, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { visualStore } from '../store/display.store';
import { loginStore } from '../store/login.store';

@Component({
  imports: [CommonModule, FormsModule],
  selector: 'language-list',
  templateUrl: './language-list.component.html',
  styleUrls: ['./language-list.component.scss']
})
export class LanguageListComponent implements OnInit {
  readonly login_store = inject(loginStore);
  readonly visual_store = inject(visualStore);

  selectedLanguage: string = "";

  ngOnInit(): void {
    this.selectedLanguage = this.login_store.settings().settings;
    this.visual_store.set_lang(this.selectedLanguage);
  }

  // supported languages
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

  onLanguageChange(selectedCode: string): void {
    this.selectedLanguage = selectedCode;
    this.visual_store.set_lang(selectedCode);
    this.login_store.load_UpdateSettings(selectedCode);
  }
}
