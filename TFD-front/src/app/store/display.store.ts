import { patchState, signalStore, withHooks, withMethods, withState } from '@ngrx/signals';
// import { inject } from '@angular/core';
// import { HttpClient } from '@angular/common/http';

export enum Selector {
  DEFAULT = "nothing",
  CHARACTERE = "CHARACTERE",
  WEAPON1 = "WEAPON1",
  WEAPON2 = "WEAPON2",
  WEAPON3 = "WEAPON3",
}

export type visuals = {
  language: string;
  searchTerms: string;
  displayOnly: string;
  isSidebarOpen: boolean;
  selector: Selector;
}

const initialVisualsState: visuals = {
  language: "ko",
  searchTerms: "",
  displayOnly: "",
  isSidebarOpen: false,
  selector: Selector.DEFAULT,
};

// view store
// this store is used to store all visual states

export const visualStore = signalStore(
  {
    providedIn: "root"
  },
  withState<visuals>(initialVisualsState),
  withMethods((visualStore) => ({
    get_lang: () => visualStore.language(),
    set_lang: (lang: string) => {
      patchState(visualStore, {language: lang})
    },
    set_search: (search: string) => {
      patchState(visualStore, {searchTerms: search})
    },
    set_sidebar: (sidebar: boolean) => {
      patchState(visualStore, {isSidebarOpen: sidebar})
    },
    set_selector: (selector: Selector) => {
      patchState(visualStore, {selector: selector})
    },
    set_displayOnly: (displayOnly: string) => {
      patchState(visualStore, {displayOnly: displayOnly})
    }
  }))
);
