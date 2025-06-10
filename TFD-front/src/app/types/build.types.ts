export interface SavedBuild {
  build_id: number;
  user_id: string;
  build_name: string;
  build_data: any;
}

export const initSavedBuild: SavedBuild = {
  build_id: 0,
  user_id: "",
  build_name: "",
  build_data: {}
}
