import { Injectable } from '@angular/core';
import { web } from '../../env/client_secret.json';

export interface GoogleUser {
  id: string;
  email: string;
  name: string;
  photoUrl: string;
}

declare const google: any;

function decodeJwt(token: string): any {
  const payload = token.split('.')[1];
  const decoded = atob(payload.replace(/-/g, '+').replace(/_/g, '/'));
  return JSON.parse(decoded);
}

@Injectable({ providedIn: 'root' })
export class GoogleAuthService {
  private initialized = false;

  init(callback: (user: GoogleUser) => void): void {
    if (this.initialized) return;
    this.initialized = true;
    google.accounts.id.initialize({
      client_id: web.client_id,
      callback: (cred: any) => {
        const data = decodeJwt(cred.credential);
        callback({
          id: data.sub,
          email: data.email,
          name: data.name,
          photoUrl: data.picture,
        });
      }
    });
    const target = document.getElementById('google-signin');
    if (target) {
      google.accounts.id.renderButton(target, { theme: 'outline', size: 'large' });
    }
  }

  signOut(): void {
    google.accounts.id.disableAutoSelect();
  }
}
