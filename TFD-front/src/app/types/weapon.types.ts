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

export interface WeaponResponse {
  id: number;
  weapon_id: number;
  weapon_name: number;   // FK translation_strings
  weapon_type_id: number;
  image_url: string;
  weapon_rarity: number;
  weapon_slot_type: number;
  available_core_slot: number;
  weapon_rounds_type_id: number; // FK translation_strings
  firearm_atk_type: number;
  firearm_atk_value: number;
  weapon_name_id: number;
  weapon_perk_ability_image_url: string;
  weapon_perk_desc_id: number;
  weapon_perk_name_id: number
  weapon_tier_id: string;
  stats?:  WeaponStat[];
  skills?: WeaponSkill[];
}

export const defaultWeapon: WeaponResponse = {
  id: 0,
  weapon_id: 0,
  weapon_name: 0, // FK translation_strings
  weapon_type_id: 0,
  image_url: "",
  weapon_rarity: 0,
  weapon_slot_type: 0,
  weapon_rounds_type_id: 0,
  available_core_slot: 0,
  firearm_atk_type: 0,
  firearm_atk_value: 0,
  weapon_name_id: 0,
  weapon_perk_ability_image_url: "",
  weapon_perk_desc_id: 0,
  weapon_perk_name_id: 0,
  weapon_tier_id: "",
  stats: undefined,
  skills: undefined,
}
