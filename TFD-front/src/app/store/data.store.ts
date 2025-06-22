import { inject } from '@angular/core';
import { signalStore, withState, withMethods, withProps, patchState } from '@ngrx/signals';
import { httpResource } from "@angular/common/http";
import { ModuleResponse } from '../types/module.types';
import { DescendantsResponse } from '../types/descendant.types';
import { WeaponResponse } from '../types/weapon.types';
import { environment } from '../../env/environment';

// translation string
export interface TranslationString {
  id:  number;
  fr:  string;
  ko:  string;
  en:  string;
  de:  string;
  jp:  string;
  zh_cn: string;
  zh_tw: string;
  it: string;
  pl: string;
  pt: string;
  ru: string;
  es: string;
}

export const defaultTranslate: TranslationString = {
  id: 0,
  fr: "",
  ko: "",
  en: "",
  de: "",
  jp: "",
  zh_cn: "",
  zh_tw: "",
  it: "",
  pl: "",
  pt: "",
  ru: "",
  es: "",
}

// cores
export interface WeaponCoreSlotOption {
  core_slot_id:   number;
  core_type:      string;  // libellé
  option_type:    string;
  option_grade:   number;
  stat:           string;  // libellé
  operator_type:  string;
  min_stat_value: number;
  max_stat_value: number;
  rate:           number;
}

export interface WeaponCoreSlots {
  weapon_id:    number;
  slot_options: WeaponCoreSlotOption[];
}

//external component
export interface ExtBaseStat {
  level:      number;
  stat_id:    number;
  stat_value: number;
}

export interface ExtSetDetail {
  set_option_id:        number;
  set_count:            number;
  set_option_effect_id: number;
}

export interface ExternalComponents {
  id:                          number;
  external_component_id:       number;
  external_component_name_id:  number;
  equipment_type_id:           number;
  image_url?:                  string;
  external_component_tier_id?: string;
  base_stat:          ExtBaseStat[];
  set_option_detail:  ExtSetDetail[];
}

//reactor
export interface ReactorBaseStat {
  level:      number;
  stat_id:    number;
  stat_value: number;
}

export interface ReactorSetDetail {
  set_option_id:        number;
  set_count:            number;
  set_option_effect_id: number;
}

export interface Reactor {
  id:                   number;
  reactor_id:           number;
  reactor_name_id:      number;
  equipment_type_id:    number;
  image_url?:           string;
  reactor_tier_id?:     string;
  base_stat:           ReactorBaseStat[];
  set_option_detail:   ReactorSetDetail[];
}

// archeron
export interface NodeEffect {
  stat_id:       number;
  stat_value:    number;
  operator_type: string;
}

export interface BoardNode {
  node_id:               number;
  name_id:               number;
  image_url:             string | null;
  node_type:             string | null;
  tier_id:               string | null;
  required_tuning_point: number | null;
  position_row:          number;
  position_column:       number;
  effects:               NodeEffect[];
}

export interface Boards {
  id: number;
  board_id: number;
  board_name_id: number;
  arche_tuning_board_id: number;
  row_size: number;
  column_size: number;
  board_image_url: string | null;
  nodes: BoardNode[];
}

export type unlock = {
  modules: boolean;
  translations: boolean;
  descendants: boolean;
  weapons: boolean;
  cores: boolean;
  externals: boolean;
  reactors: boolean;
  boards: boolean;
}

export type store = {
  modules_available: string;
  current_weapon: string;
  unlock: unlock;
}

const initunlock: unlock = {
  modules: false,
  translations: false,
  descendants: false,
  weapons: false,
  cores: false,
  externals: false,
  reactors: false,
  boards: false,
}

const initialState: store = {
  modules_available: "oui",
  current_weapon: "0",
  unlock: initunlock
};


const API_URL = environment.apiBaseUrl;

export const dataStore = signalStore(
  {
    providedIn: "root"
  },
  withState<store>(initialState),
  withProps((store) => ({
    modulesResource: httpResource<ModuleResponse[] | undefined>(() => store.unlock.modules() ? ({
        url: `${API_URL}/modules`,
        method: 'GET',
        withCredentials: true,
        transferCache: true,
      }) : undefined),
    translationResource: httpResource<TranslationString[] | undefined>(() => store.unlock.translations() ? ({
        url: `${API_URL}/translations`,
        method: 'GET',
        withCredentials: true,
        transferCache: true,
      }) : undefined),
    descendantResource: httpResource<DescendantsResponse[] | undefined>(() => store.unlock.descendants() ? ({
      url: `${API_URL}/descendants`,
      method: 'GET',
      withCredentials: true,
      transferCache: true,
    }) : undefined),
    weaponResource: httpResource<WeaponResponse[] | undefined>(() => store.unlock.weapons() ? ({
      url: `${API_URL}/weapons`,
      method: 'GET',
      withCredentials: true,
      transferCache: true,
    }) : undefined),
    coreResource: httpResource<WeaponCoreSlots | undefined>(() => store.unlock.cores() ? ({
      url: `${API_URL}/cores/${store.current_weapon()}`,
      method: 'GET',
      withCredentials: true,
      transferCache: true,
    }) : undefined),
    externalResource: httpResource<ExternalComponents[] | undefined>(() => store.unlock.externals() ? ({
      url: `${API_URL}/external-components`,
      method: 'GET',
      withCredentials: true,
      transferCache: true,
    }) : undefined),
    reactorResource: httpResource<Reactor[] | undefined>(() => store.unlock.reactors() ? ({
      url: `${API_URL}/reactors`,
      method: 'GET',
      withCredentials: true,
      transferCache: true,
    }) : undefined),
    BoardResource: httpResource<Boards[] | undefined>(() => store.unlock.boards() ? ({
      url: `${API_URL}/boards`,
      method: 'GET',
      withCredentials: true,
      transferCache: true,
    }) : undefined),
  })),
  withMethods((store) => ({
    load_descendants: () => {
      patchState(store, { unlock: { ...store.unlock(), descendants: true } });
      store.descendantResource?.reload();
    },
    load_weapons: () => {
      patchState(store, { unlock: { ...store.unlock(), weapons: true } });
      store.weaponResource?.reload();
    },
    load_modules: () => {
      patchState(store, { unlock : { ...store.unlock(), modules: true } });
      store.modulesResource?.reload()
    },
    load_translations: () => {
      patchState(store, { unlock : { ...store.unlock(), translations: true } });
      if (!store.translationResource?.hasValue()) {
        store.translationResource?.reload()
      }
    },
    load_externals: () => {
      patchState(store, { unlock: { ...store.unlock(), externals: true } });
      store.externalResource?.reload();
    },
    load_reactors: () => {
      patchState(store, { unlock: { ...store.unlock(), reactors: true } });
      store.reactorResource?.reload();
    },
    load_boards: () => {
      patchState(store, { unlock: { ...store.unlock(), boards: true } });
      store.BoardResource?.reload();
    },
    load_all: () => {
      patchState(store, {
        unlock: {
          ...store.unlock(),
          modules: true,
          translations: true,
          descendants: true,
          weapons: true,
          cores: store.unlock().cores,
          externals: true,
          reactors: true,
          boards: store.unlock().boards
        }
      });
      store.modulesResource?.reload();
      store.translationResource?.reload();
      store.descendantResource?.reload();
      store.weaponResource?.reload();
      store.externalResource?.reload();
      store.reactorResource?.reload();
      if (store.unlock().boards) {
        store.BoardResource?.reload();
      }
    },
    refresh_modules: () => store.modulesResource?.reload(),
    refresh_translation: () => store.translationResource?.reload(),
    refresh_descendants: () => store.descendantResource?.reload(),
    refresh_externals: () => store.externalResource?.reload(),
    refresh_reactors: () => store.reactorResource?.reload(),
    refresh_boards: () => store.BoardResource?.reload(),
  }))
);
