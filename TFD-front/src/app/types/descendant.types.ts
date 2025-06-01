import {ModuleResponse} from './module.types';

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

export interface DescendantsResponse {
  id: number;
  descendant_id: number;
  descendant_name: number;   // FK translation_strings
  descendant_group_id: number;
  descendant_image_url: string;
  stats?: DescendantStat[];
  skills?: DescendantSkill[];
}

export const defaultDescendants: DescendantsResponse = {
  id: 0,
  descendant_id: 0,
  descendant_name: 0, // FK translation_strings
  descendant_group_id: 0,
  descendant_image_url: "",
  stats: undefined,
  skills: undefined
}
