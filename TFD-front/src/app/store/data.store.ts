import { inject } from '@angular/core';
import { signalStore, withState, withMethods, withHooks, patchState } from '@ngrx/signals';
import { defaultModule, Module } from '../module/module.model';
import { HttpClient } from '@angular/common/http';
import { Character } from '../character/character.model';
import { Weapon } from '../weapon/weapon.model'
import { environment } from '../../env/environnement'

//== weapon ==
export type weapon_build = {
  modules: Module[];
  weapon_id: number,
}

const default_weapon = {
  modules: [defaultModule, defaultModule, defaultModule, defaultModule, defaultModule,
            defaultModule, defaultModule, defaultModule, defaultModule, defaultModule],
  weapon_id: 211011001, // set to 0
}

// == descendant ==
export type descendant_build = {
  modules: Module[];
  descendant_id: number,
}

const default_descendant: descendant_build = {
  modules: [defaultModule, defaultModule, defaultModule, defaultModule, defaultModule, defaultModule,
            defaultModule, defaultModule, defaultModule, defaultModule, defaultModule, defaultModule],
  descendant_id: 101000001, // set to 0
}

export type store = {
  modules_available: Module[];
  descendants_available: Character[];
  weapons_available: Weapon[];
  selected_weapon_1: weapon_build,
  selected_weapon_2: weapon_build,
  selected_weapon_3: weapon_build,
  selected_descendant: descendant_build;
}

const initialState: store = {
  modules_available: [],
  descendants_available: [],
  weapons_available: [],
  selected_weapon_1: { ...default_weapon },
  selected_weapon_2: { ...default_weapon },
  selected_weapon_3: { ...default_weapon },
  selected_descendant: default_descendant
};

// data store
// this store is used to store all the data from the api

export const dataStore = signalStore(
  {
    providedIn: "root"
  },
  withHooks({
    onInit(store, http = inject(HttpClient)) {
      const apimoduleurl = `${environment.apiBaseUrl}/api/modules/ui`;
      const apidescendanturl = `${environment.apiBaseUrl}/api/descendants/ui`;
      const apiweaponurl = `${environment.apiBaseUrl}/api/weapons/ui`;

      http.get<Module[]>(apimoduleurl).subscribe(
        (modules) => patchState(store, { modules_available: modules })
      );
      http.get<Character[]>(apidescendanturl).subscribe(
        (descendants) => patchState(store, { descendants_available: descendants })
      );
      http.get<Weapon[]>(apiweaponurl).subscribe(
        (weapons) => patchState(store, { weapons_available: weapons })
      );
    }
  }),
  withState<store>(initialState),
  withMethods((store) => ({
    set_selectedDescendant: (selectedDescendant: number) => {
      patchState(store, {
        selected_descendant: {
          ...store.selected_descendant(),
          descendant_id: selectedDescendant
        }
      })
    },
    set_weapon: (id: number, index: number) => {
      const w1 = { ...store.selected_weapon_1() };
      const w2 = { ...store.selected_weapon_2() };
      const w3 = { ...store.selected_weapon_3() };

      if (index === 0) {
        w1.weapon_id = id;
      } else if (index === 1) {
        w2.weapon_id = id;
      } else if (index === 2) {
        w3.weapon_id = id;
      }
      patchState(store, {
        selected_weapon_1: w1,
        selected_weapon_2: w2,
        selected_weapon_3: w3
      });
    },
    set_build: (index: number, build: Module[]) => {
      if (build.length !== 10 && build.length !== 12) {
        return;
      }
      if (index === 0) {
        patchState(store, { selected_descendant: {
            ...store.selected_descendant(),
            modules: build
          }
        })
      } else if (index === 1) {
        patchState(store, { selected_weapon_1: {
            ...store.selected_weapon_1(),
            modules: build
          }
        })
      } else if (index === 2) {
        patchState(store, { selected_weapon_2: {
            ...store.selected_weapon_2(),
            modules: build
          }
        })
      } else if (index === 3) {
        patchState(store, { selected_weapon_3: {
            ...store.selected_weapon_3(),
            modules: build
          }
        })
      }
    }
  }))
  );
