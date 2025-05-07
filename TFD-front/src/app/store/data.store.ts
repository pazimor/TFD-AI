import { inject } from '@angular/core';
import { signalStore, withState, withMethods, withProps, patchState } from '@ngrx/signals';
import { httpResource } from "@angular/common/http";
import { environment } from '../../env/environnement';

export type store = {
  modules_available: string;
}

const initialState: store = {
  modules_available: "oui"
};

export const dataStore = signalStore(
  {
    providedIn: "root"
  },

  withProps((store) => ({
    /*
    fullMe: httpResource<Module[] | undefined>(() =>
        store._resourceEnabled()
          ? {
              url: `/api/me/full`,
              method: 'GET',
              withCredentials: true,
              transferCache: true,
            }
          : undefined
        )
    */
    })),
  withState<store>(initialState),
  withMethods((store) => ({

  }))
);
