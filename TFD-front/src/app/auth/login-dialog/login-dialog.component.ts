import {Component, inject, OnInit} from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  SocialAuthService,
  SocialUser,
  GoogleLoginProvider,
  GoogleSigninButtonDirective
} from '@abacritt/angularx-social-login';
import { visualStore } from '../../store/display.store';
import { MatDialog } from '@angular/material/dialog';
import { LoginComponent } from '../login/login.component';
import {loginStore} from '../../store/login.store';

@Component({
  standalone: true,
  selector: 'login-dialog',
  imports: [CommonModule],
  templateUrl: './login-dialog.component.html',
  styleUrls: ['./login-dialog.component.scss', '../../../styles.scss']
})
export class LoginDialogComponent {
  readonly visual_store = inject(visualStore);
  readonly login_store = inject(loginStore);

  user = this.login_store.user();
  loggedIn = this.login_store.loggedIn();

  isOpen = this.visual_store.isSidebarOpen;


  constructor(
    private dialog: MatDialog) {}

  openLoginDialog(): void {
    this.dialog.open(LoginComponent, {
      width: '400px',
      autoFocus: true,
    });
  }
}
