import { bootstrapApplication } from '@angular/platform-browser';
import { AppComponent } from './app/app.component';
import { provideHttpClient } from '@angular/common/http';
import { provideAnimations } from '@angular/platform-browser/animations';
import { enableProdMode, provideExperimentalZonelessChangeDetection } from '@angular/core';

enableProdMode();

bootstrapApplication(AppComponent, {
  providers: [
    provideExperimentalZonelessChangeDetection(),
    provideHttpClient(),
    provideAnimations()
  ]
}).catch(err => console.error(err));
