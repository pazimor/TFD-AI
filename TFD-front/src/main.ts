import { bootstrapApplication } from '@angular/platform-browser';
import { AppComponent } from './app/app.component';
import {HttpClient, provideHttpClient} from '@angular/common/http';
import {APP_INITIALIZER, inject} from '@angular/core';
import {firstValueFrom, lastValueFrom, tap} from 'rxjs';

export function initApp() {
  const http = inject(HttpClient);
  return firstValueFrom(http.get('/assets/config.json').pipe(
    tap((config: any) => {
      (window as any).APP_CONFIG = config;
    })
  ));
}

bootstrapApplication(AppComponent, {
  providers: [
    provideHttpClient(),
    {
      provide: APP_INITIALIZER,
      useValue: initApp,
      deps: [HttpClient],
      multi: true
    }
  ]
}).catch(err => console.error(err));



