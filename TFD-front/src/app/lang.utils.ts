export interface UILabels {
  search: string;
  savedBuilds: string;
  buildMaker: string;
  login: string;
  logout: string;
  weapon: string;
  descendant: string;
  save: string;
}

export const uiTranslations: Record<string, UILabels> = {
  en: {
    search: 'Search',
    savedBuilds: 'Saved Builds',
    buildMaker: 'Build Maker',
    login: 'Login',
    logout: 'Logout',
    weapon: 'Weapon',
    descendant: 'Descendant',
    save: 'Save'
  },
  fr: {
    search: 'Recherche',
    savedBuilds: 'Builds sauvegardés',
    buildMaker: 'Constructeur',
    login: 'Connexion',
    logout: 'Déconnexion',
    weapon: 'Arme',
    descendant: 'Descendant',
    save: 'Sauvegarder'
  }
};

export function getUILabel(lang: string, key: keyof UILabels): string {
  const labels = uiTranslations[lang] ?? uiTranslations['en'];
  return labels[key];
}

// mapping between language codes and translation string keys
export const translationFieldMap: Record<string, string> = {
  ko: 'ko',
  en: 'en',
  de: 'de',
  ja: 'jp',
  fr: 'fr',
  'zh-CN': 'zh_cn',
  'zh-TW': 'zh_tw',
  it: 'it',
  pl: 'pl',
  pt: 'pt',
  ru: 'ru',
  es: 'es'
};
