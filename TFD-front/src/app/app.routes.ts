import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: 'my-builds',
    loadComponent: () =>
      import('./build/saved/saved-builds.component').then(m => m.SavedBuildsListComponent),
      //TODO: Add canActivate guard if authentication is required for this route
  },
  {
    path: 'build-maker',
    loadComponent: () => import('./build/main/main.component').then(c => c.MainBuildComponent)
  },
  {
    path: '',
    redirectTo: 'build-maker',
    pathMatch: 'full'
  }
];
