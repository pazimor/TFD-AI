import {inject} from '@angular/core';
import {signalStore, withState, withMethods, withHooks, patchState } from '@ngrx/signals';
import { Module } from '../module/module.model';
import { HttpClient } from '@angular/common/http';
import {Character} from '../character/character.model';


export type store = {
  language: string;
  searchTerms: string;
  modules_availables: Module[];
  selectedDescendant: number;
  descendants: Character[];
}

const initialState: store = {
  language: "ko",
  searchTerms: "",
  modules_availables: [],
  selectedDescendant: 101000001,
  descendants: []
};

export const appStore = signalStore(
  {
    providedIn: "root"
  },
  withHooks({
    onInit(store, http = inject(HttpClient)) {
      const apimoduleurl = 'http://192.168.1.35:4201/api/modules/ui';
      const apidescendanturl = 'http://192.168.1.35:4201/api/descendants/ui';

      http.get<Module[]>(apimoduleurl).subscribe(
        (modules) => patchState(store, { modules_availables: modules })
      );
      http.get<Character[]>(apidescendanturl).subscribe(
        (descendants) => patchState(store, { descendants: descendants })
      );
    }
  }),
  withState<store>(initialState),
  withMethods((store) => ({
    get_lang: () => store.language(),
    set_lang: (lang: string) => {
      patchState(store, {language: lang})
    },
    set_Search: (search: string) => {
      patchState(store, {searchTerms: search})
    },
    set_selectedDescendant: (selectedDescendant: number) => {
      patchState(store, {selectedDescendant: selectedDescendant})
    }
  }))
  );
