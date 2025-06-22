import { defaultModule } from './module.types';

export interface BuildFromDataBase {
  descendant: number;
  descendantModules: number[];
  weapons: number[];
  weaponsModules: number[][];
  reactor: number;
  externals: number[];
  boardNodes: number[];
}

export const initBuildFromDataBase: BuildFromDataBase = {
  descendant: 0,
  descendantModules: Array.from({ length: 12 }, () => 0),
  weapons: Array.from({ length: 3 }, () => 0),
  weaponsModules: Array.from({ length: 3 }, () => Array.from({ length: 10 }, () => 0)),
  reactor: 0,
  externals: Array.from({ length: 4 }, () => 0),
  boardNodes: [],
}
export interface SavedBuild {
  build_id: number;
  user_id: string;
  build_name: string;
  build_data: BuildFromDataBase;
}

export const initSavedBuild: SavedBuild = {
  build_id: 0,
  user_id: "",
  build_name: "",
  build_data: initBuildFromDataBase
}
