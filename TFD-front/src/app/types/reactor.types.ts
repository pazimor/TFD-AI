export interface ReactorBaseStat {
  level: number;
  stat_id: number;
  stat_value: number;
}

export interface ReactorSetDetail {
  set_option_id: number;
  set_count: number;
  set_option_effect_id: number;
}

export interface ReactorSkillPowerCoeff {
  coeff_stat_id: number;
  coeff_stat_value: number;
}

export interface ReactorEnchantEffect {
  enchant_level: number;
  stat_id: number;
  value: number;
}

export interface ReactorSkillPower {
  level: number;
  skill_atk_power: number;
  sub_skill_atk_power: number;
  coefficient: ReactorSkillPowerCoeff[];
  enchant_effect: ReactorEnchantEffect[];
}

export interface Reactor {
  id: number;
  reactor_id: number;
  reactor_name_id: number;
  equipment_type_id: number;
  image_url?: string;
  reactor_tier_id?: string;
  base_stat: ReactorBaseStat[];
  skill_power: ReactorSkillPower[];
  set_option_detail: ReactorSetDetail[];
}

export const defaultReactor: Reactor = {
  id: 0,
  reactor_id: 0,
  reactor_name_id: 0,
  equipment_type_id: 0,
  image_url: '',
  reactor_tier_id: '',
  base_stat: [],
  skill_power: [],
  set_option_detail: [],
};
