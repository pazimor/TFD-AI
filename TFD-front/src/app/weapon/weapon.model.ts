export interface Weapon {
  id: number;
  name: Record<string, string>;
  type: string;
  goal: string;
  capabilities: Record<string, string>;
  statistiques: Record<string, string>;
  display_data: {
    img: string;
    tier: string;
  }
}

export const defaultWeapon: Weapon = {
  id: 0,
  name: {},
  type: "",
  goal: "",
  capabilities: {},
  statistiques: {},
  display_data: {
    img: "",
    tier: "",
  }
}
