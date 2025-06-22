import { signalStore, withState, withProps, withMethods, patchState } from '@ngrx/signals';
import { httpResource } from '@angular/common/http';
import { environment } from '../../env/environment';
import { SavedBuild } from '../types/build.types';

export interface BuildListState {
  user_id: string;
  builds: SavedBuild[];
  _load: boolean;
  _delete: boolean;
  delete_id: number;
}

const initialState: BuildListState = {
  user_id: '',
  builds: [],
  _load: false, //TODO: refactor this to match data.store.ts unlock type
  _delete: false,
  delete_id: 0,
};

export const buildListStore = signalStore(
  { providedIn: 'root' },
  withState<BuildListState>(initialState),
  withProps((store) => ({
    resource: httpResource<SavedBuild[] | undefined>(() =>
      store._load()
        ? {
            url: `${environment.apiBaseUrl}/builds/${store.user_id()}`,
            method: 'GET',
            withCredentials: true,
            transferCache: true,
          }
        : undefined,
    ),
    deleteResource: httpResource<{success: boolean}>(() =>
      store._delete()
        ? {
            url: `${environment.apiBaseUrl}/build/${store.delete_id()}`,
            method: 'DELETE',
            withCredentials: true,
          }
        : undefined,
    ),
  })),
  withMethods((store) => ({
    load: (userId: string) => {
      patchState(store, { user_id: userId, _load: true });
      store.resource.reload();
    },
    deleteBuild: (id: number) => {
      patchState(store, { delete_id: id, _delete: true });
      store.deleteResource.reload();
      //TODO: find a way to clean state after resources loaded
      //patchState(store, { delete_id: 0, _delete: false });
    },
    refresh: () => {
      store.resource.reload();
    },
  })),
);
