import { inject, Injector} from '@angular/core';
import {signalStore, withState, withMethods, withProps, patchState} from '@ngrx/signals';
import { httpResource } from "@angular/common/http";
import { environment } from '../../env/environment';
import { SocialUser } from '@abacritt/angularx-social-login';

export type settingsResponse = {
  settings: string,
  success: boolean
}

export type loginStore = {
  user: SocialUser | undefined,
  settings: settingsResponse,
  _resourceEnabled: boolean,
  loggedIn: boolean
}

const initsettings: settingsResponse = {
  settings: "ko",
  success: false //TODO: delete
}

const initialState: loginStore = {
  user: undefined,
  settings: initsettings,
  _resourceEnabled: false,
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

const request = (injector: Injector, url: string, method: string, body: any) => {
  return httpResource<settingsResponse>(
    () => ({
      url,
      method,
      body,
      withCredentials: true,
    }),
    { injector },
  );
}

export const loginStore = signalStore(
  {
    providedIn: "root"
  },
  withState<loginStore>(initialState),
  withProps((store) => {
    const injector = inject(Injector);

    return {
      userSettingsResource: (user: userData) =>
        request(
          injector,
          'http://127.0.0.1:4201/api/user_settings',
          'POST',
          user,
        ),

      updateSettingsResource: (lang: string) =>
        request(
          injector,
          'http://127.0.0.1:4201/api/set_settings',
          'POST',
          { id: store.user()?.id, lang },
        ),
    };
  }),
  withMethods((store) => ({
    setLoginState: (log: SocialUser | undefined) => {
      patchState(store, { user: log, loggedIn: !!log });
    },
    setSettingsState: (set: settingsResponse | undefined) => {
      patchState(store, {settings: set});
    },
    fetchUserSettings: () => {
      const data: userData = {
        id: store.user()?.id ?? '',
        email: store.user()?.email ?? '',
        name: store.user()?.name ?? '',
        photoUrl: store.user()?.photoUrl ?? '',
      };
      return store.userSettingsResource(data);
    },
    updateUserLang: (lang: string) => {
      store.updateSettingsResource(lang)
      patchState(store, {
        settings: {
          ...store.settings(),
          settings: lang
        }
      });
    }
  }))
);
