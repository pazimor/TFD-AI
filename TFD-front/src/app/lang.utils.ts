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
  },
  ko: {
    search: '검색',
    savedBuilds: '저장된 빌드',
    buildMaker: '빌드 생성기',
    login: '로그인',
    logout: '로그아웃',
    weapon: '무기',
    descendant: '디센던트',
    save: '저장'
  },
  de: {
    search: 'Suche',
    savedBuilds: 'Gespeicherte Builds',
    buildMaker: 'Build-Editor',
    login: 'Anmelden',
    logout: 'Abmelden',
    weapon: 'Waffe',
    descendant: 'Nachfahre',
    save: 'Speichern'
  },
  ja: {
    search: '検索',
    savedBuilds: '保存されたビルド',
    buildMaker: 'ビルド作成',
    login: 'ログイン',
    logout: 'ログアウト',
    weapon: '武器',
    descendant: 'ディセンダント',
    save: '保存'
  },
  'zh-CN': {
    search: '搜索',
    savedBuilds: '已保存的构建',
    buildMaker: '构建生成器',
    login: '登录',
    logout: '登出',
    weapon: '武器',
    descendant: '后裔',
    save: '保存'
  },
  'zh-TW': {
    search: '搜尋',
    savedBuilds: '已儲存的構建',
    buildMaker: '構建產生器',
    login: '登入',
    logout: '登出',
    weapon: '武器',
    descendant: '後裔',
    save: '儲存'
  },
  it: {
    search: 'Cerca',
    savedBuilds: 'Build Salvate',
    buildMaker: 'Creatore di Build',
    login: 'Accedi',
    logout: 'Disconnetti',
    weapon: 'Arma',
    descendant: 'Discendente',
    save: 'Salva'
  },
  pl: {
    search: 'Szukaj',
    savedBuilds: 'Zapisane Buildy',
    buildMaker: 'Kreator Buildów',
    login: 'Zaloguj',
    logout: 'Wyloguj',
    weapon: 'Broń',
    descendant: 'Potomek',
    save: 'Zapisz'
  },
  pt: {
    search: 'Buscar',
    savedBuilds: 'Builds Salvos',
    buildMaker: 'Construtor de Build',
    login: 'Entrar',
    logout: 'Sair',
    weapon: 'Arma',
    descendant: 'Descendente',
    save: 'Salvar'
  },
  ru: {
    search: 'Поиск',
    savedBuilds: 'Сохранённые сборки',
    buildMaker: 'Создатель сборки',
    login: 'Войти',
    logout: 'Выйти',
    weapon: 'Оружие',
    descendant: 'Наследник',
    save: 'Сохранить'
  },
  es: {
    search: 'Buscar',
    savedBuilds: 'Construcciones guardadas',
    buildMaker: 'Creador de Builds',
    login: 'Iniciar sesión',
    logout: 'Cerrar sesión',
    weapon: 'Arma',
    descendant: 'Descendiente',
    save: 'Guardar'
  }
};

export function getUILabel(lang: string, key: keyof UILabels): string {
  const labels = uiTranslations[lang] ?? uiTranslations['en'];
  return labels[key];
}

export function getTranslationField(lang: string): string {
  switch (lang) {
    case 'ko':
    case 'en':
    case 'de':
    case 'fr':
    case 'it':
    case 'pl':
    case 'pt':
    case 'ru':
    case 'es':
      return lang;
    case 'ja':
      return 'jp';
    case 'zh-CN':
      return 'zh_cn';
    case 'zh-TW':
      return 'zh_tw';
    default:
      return 'en';
  }
}
