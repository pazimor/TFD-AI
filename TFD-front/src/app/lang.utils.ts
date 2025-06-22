export interface UILabels {
  search: string;
  savedBuilds: string;
  buildMaker: string;
  login: string;
  logout: string;
  weapon: string;
  descendant: string;
  save: string;
  buildNamePlaceholder: string;
  loadingBuilds: string;
  errorLoadingBuilds: string;
  noBuilds: string;
  refresh: string;
  wipMessage: string;
  confirmDelete: string;
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
    save: 'Save',
    buildNamePlaceholder: 'Build Name',
    loadingBuilds: 'Loading builds...',
    errorLoadingBuilds: 'Error loading builds',
    noBuilds: 'No builds found',
    refresh: 'Refresh',
    wipMessage: 'Work in progress',
    confirmDelete: 'Are you sure you want to delete this build?'
  },
  fr: {
    search: 'Recherche',
    savedBuilds: 'Builds sauvegardés',
    buildMaker: 'Constructeur',
    login: 'Connexion',
    logout: 'Déconnexion',
    weapon: 'Arme',
    descendant: 'Descendant',
    save: 'Sauvegarder',
    buildNamePlaceholder: 'Nom du build',
    loadingBuilds: 'Chargement des builds...',
    errorLoadingBuilds: "Erreur lors du chargement des builds",
    noBuilds: 'Aucun build disponible',
    refresh: 'Rafraîchir',
    wipMessage: 'Travail en cours',
    confirmDelete: 'Êtes-vous sûr de vouloir supprimer ce build ?'
  },
  ko: {
    search: '검색',
    savedBuilds: '저장된 빌드',
    buildMaker: '빌드 생성기',
    login: '로그인',
    logout: '로그아웃',
    weapon: '무기',
    descendant: '디센던트',
    save: '저장',
    buildNamePlaceholder: '빌드 이름',
    loadingBuilds: '빌드 불러오는 중...',
    errorLoadingBuilds: '빌드를 불러오는 데 오류 발생',
    noBuilds: '저장된 빌드가 없습니다',
    refresh: '새로고침',
    wipMessage: '작업 진행 중',
    confirmDelete: '이 빌드를 삭제하시겠습니까?'
  },
  de: {
    search: 'Suche',
    savedBuilds: 'Gespeicherte Builds',
    buildMaker: 'Build-Editor',
    login: 'Anmelden',
    logout: 'Abmelden',
    weapon: 'Waffe',
    descendant: 'Nachfahre',
    save: 'Speichern',
    buildNamePlaceholder: 'Build-Name',
    loadingBuilds: 'Builds werden geladen...',
    errorLoadingBuilds: 'Fehler beim Laden der Builds',
    noBuilds: 'Keine Builds gefunden',
    refresh: 'Aktualisieren',
    wipMessage: 'In Arbeit',
    confirmDelete: 'Möchten Sie diesen Build wirklich löschen?'
  },
  ja: {
    search: '検索',
    savedBuilds: '保存されたビルド',
    buildMaker: 'ビルド作成',
    login: 'ログイン',
    logout: 'ログアウト',
    weapon: '武器',
    descendant: 'ディセンダント',
    save: '保存',
    buildNamePlaceholder: 'ビルド名',
    loadingBuilds: 'ビルドを読み込み中...',
    errorLoadingBuilds: 'ビルドの読み込みエラー',
    noBuilds: 'ビルドが見つかりません',
    refresh: '更新',
    wipMessage: '作業中',
    confirmDelete: 'このビルドを削除してよろしいですか？'
  },
  'zh-CN': {
    search: '搜索',
    savedBuilds: '已保存的构建',
    buildMaker: '构建生成器',
    login: '登录',
    logout: '登出',
    weapon: '武器',
    descendant: '后裔',
    save: '保存',
    buildNamePlaceholder: '构建名称',
    loadingBuilds: '正在加载构建...',
    errorLoadingBuilds: '加载构建时出错',
    noBuilds: '没有找到构建',
    refresh: '刷新',
    wipMessage: '开发中',
    confirmDelete: '确定要删除此构建吗？'
  },
  'zh-TW': {
    search: '搜尋',
    savedBuilds: '已儲存的構建',
    buildMaker: '構建產生器',
    login: '登入',
    logout: '登出',
    weapon: '武器',
    descendant: '後裔',
    save: '儲存',
    buildNamePlaceholder: '構建名稱',
    loadingBuilds: '載入構建中...',
    errorLoadingBuilds: '載入構建時出錯',
    noBuilds: '沒有找到構建',
    refresh: '重新整理',
    wipMessage: '開發中',
    confirmDelete: '確定要刪除此構建嗎？'
  },
  it: {
    search: 'Cerca',
    savedBuilds: 'Build Salvate',
    buildMaker: 'Creatore di Build',
    login: 'Accedi',
    logout: 'Disconnetti',
    weapon: 'Arma',
    descendant: 'Discendente',
    save: 'Salva',
    buildNamePlaceholder: 'Nome build',
    loadingBuilds: 'Caricamento build...',
    errorLoadingBuilds: 'Errore nel caricamento delle build',
    noBuilds: 'Nessuna build trovata',
    refresh: 'Aggiorna',
    wipMessage: 'Lavori in corso',
    confirmDelete: 'Sei sicuro di voler eliminare questa build?'
  },
  pl: {
    search: 'Szukaj',
    savedBuilds: 'Zapisane Buildy',
    buildMaker: 'Kreator Buildów',
    login: 'Zaloguj',
    logout: 'Wyloguj',
    weapon: 'Broń',
    descendant: 'Potomek',
    save: 'Zapisz',
    buildNamePlaceholder: 'Nazwa builda',
    loadingBuilds: 'Ładowanie buildów...',
    errorLoadingBuilds: 'Błąd ładowania buildów',
    noBuilds: 'Brak zapisanych buildów',
    refresh: 'Odśwież',
    wipMessage: 'Prace w toku',
    confirmDelete: 'Czy na pewno chcesz usunąć ten build?'
  },
  pt: {
    search: 'Buscar',
    savedBuilds: 'Builds Salvos',
    buildMaker: 'Construtor de Build',
    login: 'Entrar',
    logout: 'Sair',
    weapon: 'Arma',
    descendant: 'Descendente',
    save: 'Salvar',
    buildNamePlaceholder: 'Nome do build',
    loadingBuilds: 'Carregando builds...',
    errorLoadingBuilds: 'Erro ao carregar builds',
    noBuilds: 'Nenhum build encontrado',
    refresh: 'Atualizar',
    wipMessage: 'Em desenvolvimento',
    confirmDelete: 'Tem certeza de que deseja excluir este build?'
  },
  ru: {
    search: 'Поиск',
    savedBuilds: 'Сохранённые сборки',
    buildMaker: 'Создатель сборки',
    login: 'Войти',
    logout: 'Выйти',
    weapon: 'Оружие',
    descendant: 'Наследник',
    save: 'Сохранить',
    buildNamePlaceholder: 'Название билда',
    loadingBuilds: 'Загрузка билдов...',
    errorLoadingBuilds: 'Ошибка загрузки билдов',
    noBuilds: 'Билды не найдены',
    refresh: 'Обновить',
    wipMessage: 'В разработке',
    confirmDelete: 'Вы уверены, что хотите удалить этот билд?'
  },
  es: {
    search: 'Buscar',
    savedBuilds: 'Construcciones guardadas',
    buildMaker: 'Creador de Builds',
    login: 'Iniciar sesión',
    logout: 'Cerrar sesión',
    weapon: 'Arma',
    descendant: 'Descendiente',
    save: 'Guardar',
    buildNamePlaceholder: 'Nombre de la build',
    loadingBuilds: 'Cargando builds...',
    errorLoadingBuilds: 'Error al cargar las builds',
    noBuilds: 'No se encontraron builds',
    refresh: 'Actualizar',
    wipMessage: 'Trabajo en progreso',
    confirmDelete: '¿Estás seguro de que deseas eliminar esta build?'
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
