# AGENT.MD - Frontend

## Technology
- Angular 19 (TypeScript, standalone components)
- NgRx Signals for store
- Material UI for dialogs/tabs
- Modern CSS (SCSS, responsive)

## State Management
- All global state managed via Signals, no Observables
- Stores: `data.store.ts`, `display.store.ts`, `login.store.ts`
- Prefer computed signals for derived data
- try to mimic the existing coding style

## Project Structure
```
TFD-front/
└── src/
    ├── app/
    │   ├── build/            # build UI (weapon/module/descendant)
    │   ├── store/            # NgRx signal stores
    │   ├── auth/             # Login components/dialogs
    │   ├── langlist/         # Language selector
    │   └── sidebar/          # Sidebar UI
    ├── assets/               # images, fonts, config
    ├── env/                  # environment files (API url)
    └── styles.scss           # global styles
```

## Key Conventions
- Use standalone components (`standalone: true`)
- Signal stores pattern (see `store/*.ts`)
- Use modern Angular patterns (signals over observables)
- All user-facing strings should be translatable (i18n ready)
- HTTP requests must be defined as `httpResource` objects inside stores.
- Do **not** inject `HttpClient` directly anywhere else.

## Development
- Use `ng serve` for local dev (`http://localhost:4200`)
- Docker build: compiles Angular, static files served by NGINX

## Best Practices
- Use `@for` instead of `*ngFor` for better performance in Angular 19
- Use last features of the framework when needed
- Always use explicit typing
- Follow Angular CLI scaffolding for new components
- Use `environment.ts`/`environment.prod.ts` for switching API endpoints
- Declare all interfaces and custom types in a file within `src/app/types`
  (create a new one if needed)

## Patterns
- Each store is created with `signalStore` using `withState`, `withProps` and
  `withMethods`.
- HTTP calls are defined as `httpResource` properties inside stores and
  triggered via `.reload()`.
- Default objects like `defaultModule` or `defaultWeapon` initialize state to
  avoid undefined values.
- API base URLs come from the environment files.

## PR/Commit Guidelines
- All commit / PR messages / branch name in English
- Link changes to related feature/bug in message
