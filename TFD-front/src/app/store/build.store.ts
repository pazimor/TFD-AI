import { signalStore, withState, withMethods, patchState } from '@ngrx/signals';
import { ModuleResponse, defaultModule } from '../types/module.types';
import { DescendantsResponse, defaultDescendants } from '../types/descendant.types';
import { WeaponResponse, defaultWeapon } from '../types/weapon.types';
import { Reactor, defaultReactor } from '../types/reactor.types';
import { ExternalComponent, defaultExternalComponent } from '../types/external.types';

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
  }))
);
