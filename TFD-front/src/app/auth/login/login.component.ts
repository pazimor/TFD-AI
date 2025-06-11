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
import {HttpErrorResponse, HttpResourceRef} from '@angular/common/http';
import { getUILabel } from '../../lang.utils';

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

  error: HttpErrorResponse | undefined;

  dialogStartedStatus= this.login_store.loggedIn();
  settings: any = {};

  constructor(
    private authService: SocialAuthService,
    private dialogRef: MatDialogRef<LoginComponent>) {

    this.login_store.load_UserSettings()

    effect(() => {
      if (!this.login_store.loggedIn()) return;

      if (this.login_store.userSettings_Resource.error()) {
        this.error = this.login_store.userSettings_Resource.error() as HttpErrorResponse;
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

  label(key: Parameters<typeof getUILabel>[1]) {
    return getUILabel(this.visual_store.get_lang(), key);
  }
}
