export interface Module {
    id: number;
    name: string;
    type: string;
    statistiques: string;
    optional_statistiques: string;
    stack_id: string
    stack_description: string;
    display_data: {
        img: string;
        tier: string;
    }
    drag: boolean;
}
