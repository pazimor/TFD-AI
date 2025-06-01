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
  available_descendant_id: string;
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
  available_descendant_id: "0",
  available_module_slot_type_id: undefined,
  stats: undefined,
}
