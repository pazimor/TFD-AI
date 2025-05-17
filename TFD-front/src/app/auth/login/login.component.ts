import {Component, effect, inject, OnInit, ResourceStatus} from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  SocialAuthService,
  SocialUser,
  GoogleLoginProvider,
  GoogleSigninButtonDirective
} from '@abacritt/angularx-social-login';
import { visualStore } from '../../store/display.store';
import { MatDialogRef } from '@angular/material/dialog';
import {initialUserData, loginStore, settingsResponse, userData} from '../../store/login.store';
import { LanguageListComponent } from '../../langlist/language-list.component';
import {HttpResourceRef} from '@angular/common/http';

@Component({
  standalone: true,
  selector: 'login',
  imports: [CommonModule, GoogleSigninButtonDirective, LanguageListComponent],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {
  readonly visual_store = inject(visualStore);
  readonly login_store = inject(loginStore);

  isOpen = this.visual_store.isSidebarOpen;
  dialogStartedStatus= this.login_store.loggedIn();
  userdata: userData = initialUserData;
  settings: any = {};

  private settingsRes: HttpResourceRef<settingsResponse | undefined> | undefined;

  constructor(
    private authService: SocialAuthService,
    private dialogRef: MatDialogRef<LoginComponent>) {
    effect(() => {
      if (!this.login_store.loggedIn()) return;

      if (!this.settingsRes) {
        this.settingsRes = this.login_store.fetchUserSettings();
      }

      switch (this.settingsRes.status()) {
        case ResourceStatus.Resolved:
          this.settings = this.settingsRes.value();
          this.login_store.setSettingsState(this.settingsRes.value());
          break;
      }
    });
  }

  ngOnInit() {

    this.authService.authState.subscribe((user) => {
      this.login_store.setLoginState(user)
      if(this.dialogStartedStatus !== !!user) {
        this.dialogRef.close();
      }
    });
  }

  signOut(): void {
    this.authService.signOut();
  }
}
