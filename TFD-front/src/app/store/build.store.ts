import { signalStore, withState, withMethods, patchState, withProps } from '@ngrx/signals';
import { httpResource } from '@angular/common/http';
import { ModuleResponse, defaultModule } from '../types/module.types';
import { DescendantsResponse, defaultDescendants, unsetDescendants } from '../types/descendant.types';
import { WeaponResponse, defaultWeapon } from '../types/weapon.types';
import { Reactor, defaultReactor } from '../types/reactor.types';
import { ExternalComponent, defaultExternalComponent } from '../types/external.types';
import { environment } from '../../env/environment';
import { SavedBuild, initSavedBuild, BuildFromDataBase } from '../types/build.types';

export interface BuildToHydrate {
  descendant: DescendantsResponse;
  descendantModules: ModuleResponse[];
  weapons: WeaponResponse[];
  weaponsModules: ModuleResponse[][];
  reactor: Reactor;
  externals: ExternalComponent[];
  boardNodes: number[];
}

export interface BuildState {
  descendant: DescendantsResponse;
  descendantModules: ModuleResponse[];
  weapons: WeaponResponse[];
  weaponsModules: ModuleResponse[][];
  reactor: Reactor;
  externals: ExternalComponent[];
  boardNodes: number[];
  _load_build: boolean;
  _save_build: boolean;
  currentBuild: SavedBuild;
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
  boardNodes: [],
  _load_build: false,
  _save_build: false,
  currentBuild: initSavedBuild
};

export const buildStore = signalStore(
  {
    providedIn: 'root'
  },
  withState<BuildState>(initialBuildState),
  withMethods((store) => ({
    serialize: (): BuildFromDataBase => ({
      descendant: store.descendant().descendant_id,
      descendantModules: store.descendantModules().map(module => module.module_id),
      weapons: store.weapons().map(weapons => weapons.weapon_id ),
      weaponsModules: store.weaponsModules().map(weapons => weapons.map(module => module.module_id)),
      reactor: store.reactor().reactor_id,
      externals: store.externals().map(compo => compo.external_component_id),
      boardNodes: store.boardNodes(),
    }),
    hydrate: (build: BuildToHydrate) => {
      patchState(store, {
        descendant: build.descendant,
        descendantModules: build.descendantModules,
        weapons: build.weapons,
        weaponsModules: build.weaponsModules,
        reactor: build.reactor,
        externals: build.externals,
        boardNodes: build.boardNodes,
      })
    },
  })),
  withProps((store) => ({
    getBuildRessource: httpResource<SavedBuild | undefined>(() =>
      store._load_build() && store.currentBuild().build_id > 0
        ? {
          url: `${environment.apiBaseUrl}/build/${store.currentBuild().build_id}`,
          method: 'GET',
          withCredentials: true,
          transferCache: true,
        }
        : undefined,
    ),
    SaveBuildResource: httpResource<SavedBuild | undefined>(() =>
      store._save_build()
        ? {
            url: `${environment.apiBaseUrl}/builds`,
            method: 'POST',
            body: store.currentBuild(),
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
    setBoardNodes: (nodes: number[]) => {
      patchState(store, { boardNodes: nodes });
    },
    loadFromApi: (id: number) => {
      patchState(store, { currentBuild: { ...store.currentBuild(), build_id: id }, _load_build: true });
      store.getBuildRessource.reload();
      if (store.getBuildRessource.hasValue()) {
        const saved = store.getBuildRessource.value()!;
        patchState(store, { currentBuild: saved });
      }
    },
    saveToApi: (userId: string, name: string) => {
      patchState(store, { currentBuild: {
        ...store.currentBuild(), user_id: userId, build_name: name, build_data: store.serialize()
        }, _save_build: true });
      store.SaveBuildResource.reload();
    },
    setBuildID: (id: number) => {
      patchState(store, { currentBuild: { ...store.currentBuild(), build_id: id } , _load_build: false });
    }
  }))
);
