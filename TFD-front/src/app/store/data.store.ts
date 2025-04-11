import { inject } from '@angular/core';
import { signalStore, withState, withMethods, withHooks, patchState } from '@ngrx/signals';
import { defaultModule, Module } from '../module/module.model';
import { HttpClient } from '@angular/common/http';
import { Character } from '../character/character.model';
import { Weapon } from '../weapon/weapon.model';
import { environment } from '../../env/environnement';

//== weapon ==
export type weapon_build = {
  modules: Module[];
  weapon_id: number;
}

const default_weapon: weapon_build = {
  modules: [
    defaultModule, defaultModule, defaultModule, defaultModule, defaultModule,
    defaultModule, defaultModule, defaultModule, defaultModule, defaultModule
  ],
  weapon_id: 211011001, // par défaut
}

// == descendant ==
export type descendant_build = {
  modules: Module[];
  descendant_id: number,
}

const default_descendant: descendant_build = {
  modules: [
    defaultModule, defaultModule, defaultModule, defaultModule, defaultModule, defaultModule,
    defaultModule, defaultModule, defaultModule, defaultModule, defaultModule, defaultModule
  ],
  descendant_id: 101000001, // par défaut
}

// Nouvelle définition du store avec un tableau pour les armes.
export type store = {
  modules_available: Module[];
  descendants_available: Character[];
  weapons_available: Weapon[];
  selected_weapons: weapon_build[]; // tableau de 3 armes
  selected_descendant: descendant_build;
}

const initialState: store = {
  modules_available: [],
  descendants_available: [],
  weapons_available: [],
  selected_weapons: [
    { ...default_weapon },
    { ...default_weapon },
    { ...default_weapon }
  ],
  selected_descendant: default_descendant
};

// data store
// Ce store contient toutes les données de l'API
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
      });
    },
    // Mise à jour d'une arme dans le tableau selected_weapons
    set_weapon: (id: number, index: number) => {
      const weapons = store.selected_weapons();
      if (index < 0 || index >= weapons.length) {
        return;
      }
      const updatedWeapon = { ...weapons[index], weapon_id: id };
      const updatedWeapons = weapons.map((w, idx) =>
        idx === index ? updatedWeapon : w
      );
      patchState(store, { selected_weapons: updatedWeapons });
    },
    // Mise à jour du build (les modules) soit pour le descendant ou pour une arme
    set_build: (index: number, build: Module[]) => {
      if (build.length !== 10 && build.length !== 12) {
        return;
      }
      if (index === 0) {
        patchState(store, { selected_descendant: {
            ...store.selected_descendant(),
            modules: build
          }
        });
      } else if (index >= 1 && index <= 3) {
        // Pour les armes, on considère l'indice dans le tableau comme index - 1.
        const weaponIndex = index - 1;
        const weapons = store.selected_weapons();
        if (weaponIndex < 0 || weaponIndex >= weapons.length) {
          return;
        }
        const updatedWeapon = { ...weapons[weaponIndex], modules: build };
        const updatedWeapons = weapons.map((w, idx) =>
          idx === weaponIndex ? updatedWeapon : w
        );
        patchState(store, { selected_weapons: updatedWeapons });
      }
    }
  }))
);
