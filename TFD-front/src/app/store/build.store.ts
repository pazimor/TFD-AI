import { signalStore, withState, withMethods, patchState } from '@ngrx/signals';
import { inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ModuleResponse, defaultModule } from '../types/module.types';
import { DescendantsResponse, defaultDescendants } from '../types/descendant.types';
import { WeaponResponse, defaultWeapon } from '../types/weapon.types';
import { Reactor, defaultReactor } from '../types/reactor.types';
import { ExternalComponent, defaultExternalComponent } from '../types/external.types';
import { environment } from '../env/environment';
import { SavedBuild } from '../types/build.types';

export interface BuildState {
  descendant: DescendantsResponse;
  descendantModules: ModuleResponse[];
  weapons: WeaponResponse[];
  weaponsModules: ModuleResponse[][];
  reactor: Reactor;
  externals: ExternalComponent[];
}

const initialBuildState: BuildState = {
  descendant: defaultDescendants,
  descendantModules: Array.from({ length: 12 }, () => ({ ...defaultModule })),
  weapons: Array.from({ length: 3 }, () => ({ ...defaultWeapon })),
  weaponsModules: Array.from({ length: 3 }, () =>
    Array.from({ length: 10 }, () => ({ ...defaultModule }))
  ),
  reactor: defaultReactor,
  externals: Array.from({ length: 4 }, () => ({ ...defaultExternalComponent })),
};

export const buildStore = signalStore(
  {
    providedIn: 'root'
  },
  withState<BuildState>(initialBuildState),
  withMethods((store) => {
    const http = inject(HttpClient);
    return {
    setDescendant: (desc: DescendantsResponse) => {
      patchState(store, { descendant: desc });
    },
    updateDescendantModule: (index: number, module: ModuleResponse) => {
      const modules = [...store.descendantModules()];
      modules[index] = module;
      patchState(store, { descendantModules: modules });
    },
    setWeaponAt: (index: number, weapon: WeaponResponse) => {
      const weapons = [...store.weapons()];
      weapons[index] = weapon;
      patchState(store, { weapons });
    },
    updateWeaponModule: (weaponIndex: number, moduleIndex: number, module: ModuleResponse) => {
      const moduleArrays = store.weaponsModules().map(arr => [...arr]);
      moduleArrays[weaponIndex][moduleIndex] = module;
      patchState(store, { weaponsModules: moduleArrays });
    },
    setReactor: (reactor: Reactor) => {
      patchState(store, { reactor });
    },
    setExternal: (index: number, external: ExternalComponent) => {
      const externals = [...store.externals()];
      externals[index] = external;
      patchState(store, { externals });
    },
    serialize: () => ({
      descendant: store.descendant(),
      descendantModules: store.descendantModules(),
      weapons: store.weapons(),
      weaponsModules: store.weaponsModules(),
      reactor: store.reactor(),
      externals: store.externals(),
    }),
    load: (data: BuildState) => {
      patchState(store, data);
    },
    loadFromApi: (id: number) => {
      http
        .get<SavedBuild>(`${environment.apiBaseUrl}/build/${id}`, {
          withCredentials: true,
        })
        .subscribe((res) => {
          patchState(store, res.build_data as BuildState);
        });
    },
  }))
);
