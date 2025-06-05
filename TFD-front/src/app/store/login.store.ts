import { inject, Injector} from '@angular/core';
import {signalStore, withState, withMethods, withProps, patchState} from '@ngrx/signals';
import { httpResource } from "@angular/common/http";
import { environment } from '../../env/environment';
import { SocialUser } from '@abacritt/angularx-social-login';
import { visualStore } from './display.store';

const display = inject(visualStore);

export type settingsResponse = {
  settings: string,
  success: boolean
}

export type loginStore = {
  user: SocialUser | undefined,
  settings: settingsResponse,
  _userSettingsResourceEnabled: boolean,
  _updateSettingsResourceEnabled: boolean,
  loggedIn: boolean
}

const initsettings: settingsResponse = {
  settings: "ko",
  success: false //TODO: delete
}

const initialState: loginStore = {
  user: undefined,
  settings: initsettings,
  _userSettingsResourceEnabled: false,
  _updateSettingsResourceEnabled: false,
  loggedIn: false
};

export type userData = {
  id: string;
  name : string;
  email: string;
  photoUrl: string;
}

export const initialUserData: userData = {
  id: "",
  name : "",
  email: "",
  photoUrl: ""
}

export const loginStore = signalStore(
  {
    providedIn: "root"
  },
  withState<loginStore>(initialState),
  withProps((store) => ({
      userSettings_Resource: httpResource<settingsResponse | undefined>(() =>
        store._userSettingsResourceEnabled()
          ? {
            url: `${environment.apiBaseUrl}/user_settings`,
            method: 'POST',
            body: {
              id: store.user()?.id ?? '',
              email: store.user()?.email ?? '',
              name: store.user()?.name ?? '',
              photoUrl: store.user()?.photoUrl ?? '',
            },
            withCredentials: true,
            transferCache: true,
          }
          : undefined),
      updateSettings_Resource: httpResource<settingsResponse | undefined> (() =>
        store._updateSettingsResourceEnabled()
          ? {
            url: `${environment.apiBaseUrl}/set_settings`,
            method: 'POST',
            body: { id: store.user()?.id,   lang: store.settings()?.settings },
            withCredentials: true,
            transferCache: true,
          }
          : undefined),
  })),
  withMethods((store) => ({
    setLoginState: (log: SocialUser | undefined) => {
      patchState(store, { user: log, loggedIn: !!log });
    },
    load_UserSettings: () => {
      if ( store.user()?.id === ''
        || store.user()?.email === ''
        || store.user()?.name === ''
        || store.user()?.photoUrl === '') {
        return;
      }
      patchState(store, { _userSettingsResourceEnabled: true });
      store.userSettings_Resource.reload();
      if (store.userSettings_Resource.hasValue()) {
        patchState(store, {
          settings: {
            ...store.userSettings_Resource.value()
          }
        });
        display.set_lang(store.userSettings_Resource.value().settings);
      }
    },
    load_UpdateSettings: (lang: string) => {
      patchState(store, {
        settings: {
          ...store.settings(), //TODO: rename (not obvious) / create new object
          settings: lang
        },
        _updateSettingsResourceEnabled: true
      });
      display.set_lang(lang);
      store.updateSettings_Resource.reload()
    },
    refresh_UserSettings: () => store.userSettings_Resource.reload(),
    refresh_UpdateSettings: () => store.updateSettings_Resource.reload(),
  }))
);
