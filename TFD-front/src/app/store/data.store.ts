import {inject} from '@angular/core';
import {signalStore, withState, withMethods, withHooks, patchState } from '@ngrx/signals';
import { Module } from '../module/module.model';
import { HttpClient } from '@angular/common/http';
import { Character } from '../character/character.model';
import { Weapon } from '../weapon/weapon.model'

const apiBaseUrl: string = (window as any).APP_CONFIG?.apiBaseUrl ?? 'https://theory-crafter-api.pazimor.dev';

export type store = {
  language: string;
  searchTerms: string;
  modules_availables: Module[];
  selectedDescendant: number;
  descendants: Character[];
  weapons: Weapon[];
}

const initialState: store = {
  language: "ko",
  searchTerms: "",
  modules_availables: [],
  selectedDescendant: 101000001,
  descendants: [],
  weapons: []
};

export const appStore = signalStore(
  {
    providedIn: "root"
  },
  withHooks({
    onInit(store, http = inject(HttpClient)) {
      const apimoduleurl = `${apiBaseUrl}/api/modules/ui`;
      const apidescendanturl = `${apiBaseUrl}/api/descendants/ui`;
      const apiweaponurl = `${apiBaseUrl}/api/weapons/ui`;

      http.get<Module[]>(apimoduleurl).subscribe(
        (modules) => patchState(store, { modules_availables: modules })
      );
      http.get<Character[]>(apidescendanturl).subscribe(
        (descendants) => patchState(store, { descendants: descendants })
      );
      http.get<Weapon[]>(apiweaponurl).subscribe(
        (weapons) => patchState(store, { weapons: weapons })
      );
    }
  }),
  withState<store>(initialState),
  withMethods((store) => ({
    get_lang: () => store.language(),
    set_lang: (lang: string) => {
      patchState(store, {language: lang})
    },
    set_search: (search: string) => {
      patchState(store, {searchTerms: search})
    },
    set_selectedDescendant: (selectedDescendant: number) => {
      patchState(store, {selectedDescendant: selectedDescendant})
    }
  }))
  );
