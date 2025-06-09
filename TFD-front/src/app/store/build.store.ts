import { signalStore, withState, withMethods, patchState, withProps } from '@ngrx/signals';
import { httpResource } from '@angular/common/http';
import { ModuleResponse, defaultModule } from '../types/module.types';
import { DescendantsResponse, defaultDescendants } from '../types/descendant.types';
import { WeaponResponse, defaultWeapon } from '../types/weapon.types';
import { Reactor, defaultReactor } from '../types/reactor.types';
import { ExternalComponent, defaultExternalComponent } from '../types/external.types';
import { environment } from '../../env/environment';
import { SavedBuild } from '../types/build.types';

export interface BuildState {
  descendant: DescendantsResponse;
  descendantModules: ModuleResponse[];
  weapons: WeaponResponse[];
  weaponsModules: ModuleResponse[][];
  reactor: Reactor;
  externals: ExternalComponent[];
  _load_build: boolean;
  _save_build: boolean;
  saveUserId: string;
  saveName: string;
  id: number;
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
  _load_build: false,
  _save_build: false,
  saveUserId: '',
  saveName: '',
  id: 0,
};

export const buildStore = signalStore(
  {
    providedIn: 'root'
  },
  withState<BuildState>(initialBuildState),
  withProps((store) => ({
    resource: httpResource<SavedBuild[] | undefined>(() =>
      store._load_build()
        ? {
          url: `${environment.apiBaseUrl}/build/${store.id}`,
          method: 'GET',
          withCredentials: true,
          transferCache: true,
        }
        : undefined,
    ),
    saveResource: httpResource<SavedBuild | undefined>(() =>
      store._save_build()
        ? {
            url: `${environment.apiBaseUrl}/builds`,
            method: 'POST',
            body: {
              user_id: store.saveUserId(),
              name: store.saveName(),
              data: store.serialize(),
            },
            withCredentials: true,
            transferCache: true,
          }
        : undefined,
    ),
  })),
  withMethods((store) => ({
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
      patchState(store, { id, _load_build: true });
      store.resource.reload();
      if (store.resource.hasValue()) {
        const saved = store.resource.value() as SavedBuild;
        patchState(store, { ...saved.build_data, id: saved.build_id });
      }
    },
    saveToApi: (userId: string, name: string) => {
      patchState(store, { saveUserId: userId, saveName: name, _save_build: true });
      store.saveResource.reload();
    },
  }))
);
