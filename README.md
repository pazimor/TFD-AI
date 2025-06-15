# TFD-AI
personal project for theory-crafting-ai tool base on the first descendant game

## Environment Variables

The backend reads the database URL from the `DB_CONN` environment variable.
The frontend expects a Google OAuth configuration stored in `CLIENT_SECRET_JSON`.
Run `npm run generate-client-secret` in `TFD-front` to create
`src/env/client_secret.json` from this variable before building the UI. This
file provides the Google client ID used by the sign-in button.

```bash
export CLIENT_SECRET_JSON="$(cat path/to/your/client_secret.json)"
```

To make Alembic work without manually exporting paths, use `./api/alembic.sh`
which sets `PYTHONPATH` correctly and forwards any arguments to `alembic`.

## Login Persistence

The frontend stores Google user information in `localStorage` under the
`googleUser` key. When the app initializes, it loads this data and syncs it with
the API so the user remains logged in after refreshing the page.

