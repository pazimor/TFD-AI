export interface Module {
    id: number;
    name: Record<string, string>;
    type: string;
    statistiques: Record<string, string>;
    optional_statistiques: string;
    stack_id: string
    stack_description: string;
    display_data: {
        img: string;
        tier: string;
    }
    drag: boolean;
}


export const defaultModule: Module = {
  id: 0,
  name: {},
  type: "",
  statistiques: {},
  optional_statistiques: "",
  stack_id: "",
  stack_description: "",
  display_data: {
    img: "",
    tier: "",
  },
  drag: true
}
