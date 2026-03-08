# Contributing

## Documentation

This repository now uses VitePress for documentation.

Docs source lives under `docs/`, and the GitHub Pages build is defined in `.github/workflows/deploy_docs.yml`.

### Installing Dependencies

```bash
npm install
```

### Local Preview

Run a local dev server:

```bash
npm run docs:dev
```

Build the static site locally:

```bash
npm run docs:build
```

Preview the production build:

```bash
npm run docs:preview
```

### Deploying

Documentation is deployed automatically to GitHub Pages when changes land on `main`.

The workflow:

1. installs Node dependencies
2. builds the VitePress site
3. uploads `docs/.vitepress/dist`
4. deploys it with the GitHub Pages actions

### Adding A New Page

1. Add the markdown file under `docs/`.
2. Add it to the sidebar in `docs/.vitepress/config.mts`.
3. If the page is JetClaw-specific, prefer placing it under `docs/jetclaw/`.
4. If the page changes robot setup or service behavior, update `README.md` at the same time.

### Updating Existing Docs

Keep these aligned:

- `README.md`
- `AGENTS.md`
- `docs/getting_started.md`
- `docs/jetclaw/waveshare-jetbot-2gb.md`
- `docs/jetclaw/picoclaw.md`
- `docs/jetclaw/operations.md`

### Updating The Changelog

We follow [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) for `CHANGELOG.md`. If a change matters to users or maintainers, consider adding an entry.
