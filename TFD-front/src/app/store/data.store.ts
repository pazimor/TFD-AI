import {inject} from '@angular/core';
import {signalStore, withState, withMethods, withHooks, patchState } from '@ngrx/signals';
import { Module } from '../module/module.model';
import { HttpClient } from '@angular/common/http';
import { Character } from '../character/character.model';
import { Weapon } from '../weapon/weapon.model'
import { environment } from '../../env/environnement'

export enum Selector {
  DEFAULT = "nothing",
  CHARACTERE = "CHARACTERE",
  WEAPON1 = "WEAPON1",
  WEAPON2 = "WEAPON2",
  WEAPON3 = "WEAPON3",
}

export type store = {
  language: string;
  searchTerms: string;
  isSidebarOpen: boolean;
  modules_availables: Module[];
  selectedDescendant: number;
  descendants: Character[];
  selectedWeapons: number[];
  weapons: Weapon[];
  selector: Selector;
}

const initialState: store = {
  language: "ko",
  searchTerms: "",
  isSidebarOpen: false,
  modules_availables: [],
  selectedDescendant: 101000001,
  descendants: [],
  selectedWeapons: [211011001, 211011001, 211011001],
  weapons: [],
  selector: Selector.DEFAULT,
};

export const appStore = signalStore(
  {
    providedIn: "root"
  },
  withHooks({
    onInit(store, http = inject(HttpClient)) {
      const apimoduleurl = `${environment.apiBaseUrl}/api/modules/ui`;
      const apidescendanturl = `${environment.apiBaseUrl}/api/descendants/ui`;
      const apiweaponurl = `${environment.apiBaseUrl}/api/weapons/ui`;

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
    set_sidebar: (sidebar: boolean) => {
      patchState(store, {isSidebarOpen: sidebar})
    },
    set_selectedDescendant: (selectedDescendant: number) => {
      patchState(store, {selectedDescendant: selectedDescendant})
    },
    set_weapon: (id: number, index: number) => {
        const newWeapons = [...store.selectedWeapons()];
        newWeapons[index] = id;
        patchState(store, {selectedWeapons: newWeapons})
    },
    set_selector: (selector: Selector) => {
      patchState(store, {selector: selector})
    }
  }))
  );
