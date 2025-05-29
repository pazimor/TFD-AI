import { inject } from '@angular/core';
import { signalStore, withState, withMethods, withProps, patchState } from '@ngrx/signals';
import { httpResource } from "@angular/common/http";

// modules
export interface ModuleStat {
  level: number;
  module_capacity: number;
  value: Record<string, unknown>; // ou un type plus précis
}

export interface ModuleResponse {
  id: number;
  module_name_id: number;
  module_name: string;
  module_id: number;
  image_url?: string;
  module_type?: number;
  module_tier_id?: string;
  module_socket_type?: string;
  module_socket_type_id?: number;
  module_class_id?: number;
  module_class?: string;
  available_weapon_type?: string;
  available_descendant_id?: string;
  available_module_slot_type_id?: string;
  stats?: ModuleStat[];
}

export const defaultModule: ModuleResponse = {
  id: 0,
  module_name_id: 0,
  module_name: "",
  module_id: 0,
  image_url: undefined,
  module_type: undefined,
  module_tier_id: undefined,
  module_socket_type: undefined,
  module_socket_type_id: undefined,
  module_class_id: undefined,
  module_class: undefined,
  available_weapon_type: undefined,
  available_descendant_id: undefined,
  available_module_slot_type_id: undefined,
  stats: undefined,
}

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

// descendant
export interface DescendantStatDetail {
  stat_id:    number;
  stat_value: number;
}

export interface DescendantStat {
  level:       number;
  stat_detail: DescendantStatDetail[];
}

export interface DescendantSkill {
  skill_type:       number;
  skill_name:       number;
  element_type:     number;
  arche_type:       number | null;
  skill_image_url:  string;
  skill_description:number;
}

export interface Descendants {
  id:                 number;
  descendant_id:      number;
  descendant_name:    number;   // FK translation_strings
  descendant_group_id:number;
  descendant_image_url:string;
  stats:  DescendantStat[];
  skills: DescendantSkill[];
}

// weapon
export interface WeaponStatDetail {
  stat_id:    number;
  stat_value: number;
}
export interface WeaponStat {
  level:       number;
  stat_detail: WeaponStatDetail[];
}
export interface WeaponSkill {
  skill_type:       number;
  skill_name:       number;
  element_type:     number;
  arche_type:       number | null;
  skill_image_url:  string;
  skill_description:number;
}
export interface Weapons {
  id:              number;
  weapon_id:       number;
  weapon_name:     number;   // FK translation_strings
  weapon_type_id:  number;
  weapon_image_url:string;
  weapon_rarity:   number;
  weapon_slot_type:number;
  stats:  WeaponStat[];
  skills: WeaponSkill[];
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
  effects:               NodeEffect[];
}

export interface Boards {
  id:              number;
  board_id:        number;
  board_name_id:   number;
  board_group_id:  number;
  board_image_url: string | null;
  nodes:           BoardNode[];
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


const API_URL = "http://localhost:4201";

export const dataStore = signalStore(
  {
    providedIn: "root"
  },
  withState<store>(initialState),
  withProps((store) => ({
    modulesResource: httpResource<ModuleResponse[] | undefined>(() => store.unlock.modules() ? ({
        url: `${API_URL}/api/modules`,
        method: 'GET',
        withCredentials: true,
        transferCache: true,
      }) : undefined),
    translationResource: httpResource<TranslationString[] | undefined>(() => store.unlock.translations() ? ({
        url: `${API_URL}/api/translations`,
        method: 'GET',
        withCredentials: true,
        transferCache: true,
      }) : undefined),
    descendantResource: httpResource<Descendants | undefined>(() => store.unlock.descendants() ? ({
      url: `${API_URL}/api/descendants`,
      method: 'GET',
      withCredentials: true,
      transferCache: true,
    }) : undefined),
    weaponResource: httpResource<Weapons | undefined>(() => store.unlock.weapons() ? ({
      url: `${API_URL}/api/weapons`,
      method: 'GET',
      withCredentials: true,
      transferCache: true,
    }) : undefined),
    coreResource: httpResource<WeaponCoreSlots | undefined>(() => store.unlock.cores() ? ({
      url: `${API_URL}/api/cores/${store.current_weapon()}`,
      method: 'GET',
      withCredentials: true,
      transferCache: true,
    }) : undefined),
    externalResource: httpResource<ExternalComponents | undefined>(() => store.unlock.externals() ? ({
      url: `${API_URL}/api/external-components`,
      method: 'GET',
      withCredentials: true,
      transferCache: true,
    }) : undefined),
    reactorResource: httpResource<Reactor | undefined>(() => store.unlock.reactors() ? ({
      url: `${API_URL}/api/reactors`,
      method: 'GET',
      withCredentials: true,
      transferCache: true,
    }) : undefined),
    Resource: httpResource<Boards | undefined>(() => store.unlock.boards() ? ({
      url: `${API_URL}/api/boards`,
      method: 'GET',
      withCredentials: true,
      transferCache: true,
    }) : undefined),
  })),
  withMethods((store) => ({
    load_modules: () => {
      patchState(store, { unlock : { ...store.unlock(), modules: true } });
      store.modulesResource?.reload()
      //patchState(store, { unlock : { ...store.unlock, modules: false } });
    },
    load_translations: () => {
      patchState(store, { unlock : { ...store.unlock(), translations: true } });
      if (!store.translationResource?.hasValue()) {
        store.translationResource?.reload()
      }
      //patchState(store, { unlock : { ...store.unlock, translations: false } });
    },
    refresh_modules: () => store.modulesResource?.reload(),
    refresh_translation: () => store.translationResource?.reload(),
    refresh_descendants: () => store.descendantResource?.reload(),
  }))
);
