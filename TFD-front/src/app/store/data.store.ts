import {inject, signal} from '@angular/core';
import {signalStore, withState, withMethods, withHooks, patchState } from '@ngrx/signals';
import { Module } from '../module/module.model';
import { HttpClient } from '@angular/common/http';
import {switchMap} from 'rxjs';


export type store = {
  language: string;
  modules_availables: Module[];
}

const initialState: store = {
  language: "ko",
  modules_availables: []
};

export const appStore = signalStore(
  {
    providedIn: "root"
  },
  withHooks({
    onInit(store, http = inject(HttpClient)) {
      const apiUrl = 'http://192.168.1.35:4201/api/modules/ui';

      http.get<Module[]>(apiUrl).subscribe(
        (modules) => patchState(store, { modules_availables: modules })
      );
    }
  }),
  withState<store>(initialState),
  withMethods((store) => ({
    get_lang: () => store.language(),
    set_lang: (lang: string) => {
      patchState(store, {language: lang})
    }
  }))
  );
