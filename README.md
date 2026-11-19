# Say it, then ship it

An El Camino College ScaleUP workshop (2026) for building with GitHub Copilot and OpenCode.

[Live discussion on Discord](https://discord.gg/sMafw3ktj)

## Run the site

Use Node.js 22.23.4 or newer and npm.

```sh
npm install
npm run dev
```

Open the URL Astro prints, including `/say-it-then-ship-it/`.

```sh
npm run check
npm run build
npm run preview
```

For browser checks, run `npx playwright install chromium` once, then `npm test` after a build.

## Keep lab content separate

`web/` contains the Astro app. `lab/` contains the workshop material.

The site renders Markdown from these locations at build time:

- `lab/**/*.md`
- `.github/agents/**/*.md`
- `.github/instructions/**/*.md`
- `.github/skills/**/*.md`
- `.agents/skills/**/*.md`
- `.opencode/**/*.md`
- `AGENTS.md`
- `.github/copilot-instructions.md`

Put agents and skills in their native locations. The site reads the same files, so you do not need a web copy. Add an optional `title`, `description`, and numeric `order` to Markdown frontmatter to control the directory listing. Agent files can use `name` in place of `title`. Without either, the site uses the filename.

Use fenced code blocks with a language for syntax highlighting. Use a `mermaid` fence for diagrams. Include `accTitle` and `accDescr` in diagrams for screen-reader context. Readers without JavaScript can read the diagram source.

The reader supports Markdown text, code fences, and Mermaid. It does not interpret Markdown links as site routes or publish adjacent images; use full repository URLs for those resources.

## Publish on GitHub Pages

The default repository target is `cristianandfriends/say-it-then-ship-it`.

1. Create a GitHub repository and push these files to its `main` branch.
2. In **Settings > Pages > Build and deployment**, select **GitHub Actions**.
3. Run **Deploy lab site**, or push a change to `main`.

The workflow builds `web/dist/` and deploys it to Pages. It reads `GITHUB_REPOSITORY` to set the source links, canonical URL, and project base path, including when you fork or rename the repository. Repositories named `<owner>.github.io` use the root path.

For a local build targeting another repository:

```sh
GITHUB_REPOSITORY=your-name/your-repo npm run build
```

Edit `web/site.config.mjs` to change the default repository, Discord invite, or slide deck.
