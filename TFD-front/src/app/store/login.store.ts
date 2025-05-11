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
  settings: "",
  success: false
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

export const loginStore = signalStore(
  {
    providedIn: "root"
  },
  withProps((store) => {
    const injector = inject(Injector);
    return {
      userlog: (user: userData) =>
        httpResource<settingsResponse>(
          () => ({
            url: 'http://127.0.0.1:4201/api/usersettings',
            method: 'POST',
            body: user,
            withCredentials: true
          }),
          {
            injector
          }
        )
    };
  }),
  withState<loginStore>(initialState),
  withMethods((store) => ({
    set_log: (log: SocialUser | undefined) => {
      patchState(store, { user: log, loggedIn: !!log });
    },
    set_settings: (set: settingsResponse | undefined) => {
      patchState(store, {settings: set});
    },
    user_settings: () => {
      const data: userData = {
        id: store.user()?.id ?? '',
        email: store.user()?.email ?? '',
        name: store.user()?.name ?? '',
        photoUrl: store.user()?.photoUrl ?? ''
      };
      return store.userlog(data)
    },
    user_langue: () => {}
  }))
);
