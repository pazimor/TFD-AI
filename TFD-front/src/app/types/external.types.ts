export interface ExtBaseStat {
  level: number;
  stat_id: number;
  stat_value: number;
}

export interface ExtSetDetail {
  set_option_id: number;
  set_count: number;
  set_option_effect_id: number;
}

export interface ExternalComponent {
  id: number;
  external_component_id: number;
  external_component_name_id: number;
  equipment_type_id: number;
  image_url?: string;
  external_component_tier_id?: string;
  base_stat: ExtBaseStat[];
  set_option_detail: ExtSetDetail[];
}

export const defaultExternalComponent: ExternalComponent = {
  id: 0,
  external_component_id: 0,
  external_component_name_id: 0,
  equipment_type_id: 0,
  image_url: '',
  external_component_tier_id: '',
  base_stat: [],
  set_option_detail: [],
};
