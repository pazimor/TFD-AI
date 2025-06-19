import { Component, effect, inject, OnInit, AfterViewInit, computed, Signal } from '@angular/core';
import { visualStore } from '../../store/display.store';
import { MatDialogRef } from '@angular/material/dialog';
import { loginStore } from '../../store/login.store';
import { LanguageListComponent } from '../../langlist/language-list.component';
import { HttpErrorResponse } from '@angular/common/http';
import { getUILabel } from '../../lang.utils';
import { GoogleAuthService, GoogleUser } from '../google-auth.service';

@Component({
  standalone: true,
  selector: 'login',
  imports: [LanguageListComponent],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit, AfterViewInit {
  readonly visual_store = inject(visualStore);
  readonly login_store = inject(loginStore);

  readonly error = computed<HttpErrorResponse | undefined>(() => {
    if (!this.login_store.loggedIn()) {
      return undefined;
    }
    const err = this.login_store.userSettings_Resource.error();
    return err ? (err as HttpErrorResponse) : undefined;
  });

  dialogStartedStatus= this.login_store.loggedIn();
  settings: any = {};

  constructor(
    private googleAuth: GoogleAuthService,
    private dialogRef: MatDialogRef<LoginComponent>) {

    this.login_store.load_UserSettings()
  }

  ngOnInit() {}

  ngAfterViewInit(): void {
    this.googleAuth.init((user: GoogleUser) => {
      this.login_store.setLoginState(user);
      this.login_store.load_UserSettings();
      if (this.dialogStartedStatus !== !!user) {
        this.dialogRef.close();
      }
    });
  }

  signOut(): void {
    this.googleAuth.signOut();
    this.login_store.setLoginState(undefined as any);
  }

  label(key: Parameters<typeof getUILabel>[1]) {
    return getUILabel(this.visual_store.get_lang(), key);
  }
}
