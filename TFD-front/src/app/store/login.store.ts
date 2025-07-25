import { effect, inject, Injector } from '@angular/core';
import {signalStore, withState, withMethods, withProps, patchState} from '@ngrx/signals';
import { httpResource } from "@angular/common/http";
import { environment } from '../../env/environment';
import { GoogleUser } from '../auth/google-auth.service';
import { visualStore } from './display.store';
import { withEffects } from '@ngrx/signals/events';

function loadStoredUser(): GoogleUser | undefined {
  const raw = localStorage.getItem('googleUser');
  if (!raw) return undefined;
  try {
    return JSON.parse(raw) as GoogleUser;
  } catch {
    return undefined;
  }
}

const storedUser = loadStoredUser();

export type settingsResponse = {
  settings: string,
  success: boolean
}

export type loginStore = {
  user: GoogleUser | undefined,
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
  user: storedUser,
  settings: initsettings,
  _userSettingsResourceEnabled: false,
  _updateSettingsResourceEnabled: false,
  loggedIn: !!storedUser
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
    display: inject(visualStore),
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
    load_UserSettings: () => {
      if ( store.user()?.id === ''
        || store.user()?.email === ''
        || store.user()?.name === ''
        || store.user()?.photoUrl === '') {
        return;
      }
      patchState(store, { _userSettingsResourceEnabled: true });
      store.userSettings_Resource.reload();
      effect(() => {
        if (store.userSettings_Resource.hasValue()) {
          store.display.set_lang(store.userSettings_Resource.value().settings);
          patchState(store, {
            settings: {
              ...store.userSettings_Resource.value()
            },
            _userSettingsResourceEnabled: false
          });
          if (store.user()?.id) {
            patchState(store, {
              user: {
                ...store.user()!,
                photoUrl: `${environment.apiBaseUrl}/user_photo/${store.user()!.id}`
              }
            });
          }
        }
      });
    },
  })),
  withMethods((store) => ({
    setLoginState: (log: GoogleUser | undefined) => {
      patchState(store, { user: log, loggedIn: !!log });
      if (log) {
        localStorage.setItem('googleUser', JSON.stringify(log));
      } else {
        localStorage.removeItem('googleUser');
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
      store.display.set_lang(lang);
      store.updateSettings_Resource.reload()
    },
    refresh_UserSettings: () => store.userSettings_Resource.reload(),
    refresh_UpdateSettings: () => store.updateSettings_Resource.reload(),
    initFromStorage: () => {
      if (storedUser) {
        store.load_UserSettings();
      }
    },
  }))
);
