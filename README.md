# Say it, then ship it

An El Camino College ScaleUP workshop (2026) for building with GitHub Copilot and OpenCode.

[Live discussion on Discord](https://discord.gg/sMafw3ktj)

## Start the lab

Follow [the lab guide](lab/start-here.md) through levels 0 to 6. Build a local Python study queue, then practice writing a skill, reviewing with another agent, and handing work to a fresh session. The last level offers a read-only MCP exercise.

Students need Python and access to PyPI. The facilitator provides the coding-agent environment and this workshop folder. Students do not need Node, Git, or the website build tools.

Use [bootstrap-lab](.agents/skills/bootstrap-lab/SKILL.md) to choose Copilot or OpenCode and install the shipped skills, the software-engineering-expert agent, and Python-only project instructions into a separate project.

```sh
python .agents/skills/bootstrap-lab/scripts/bootstrap_lab.py --harness copilot --target ../my-project
```

Use `--harness opencode` for OpenCode. Read the proposed setup before running it; the installer preserves unrelated files and refuses conflicting files.

## Maintain the website

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

The reader supports Markdown text, code fences, and Mermaid. It resolves source-relative Markdown links to reader pages, including skill references. Links to scripts and other source files open GitHub. Keep image URLs absolute; the site does not publish adjacent images. The build rejects missing local link targets.

The home page groups ordered lab levels, guides, and the skill and agent entry points. Supporting references remain readable through their links without filling the main directory.

## Check workshop tooling

```sh
python -m unittest discover -s tests -p "test_*.py"
```

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
