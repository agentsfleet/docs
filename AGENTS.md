# Documentation project instructions

> The operating model is global: every agent home symlinks to
> `~/Projects/dotfiles/AGENTS.md`; rule pages and gates resolve from that
> checkout. This file carries only project facts. Drive work with `orly gate`.


## About this project

- This is the agentsfleet documentation site built on [Mintlify](https://mintlify.com)
- Pages are MDX files with YAML frontmatter
- Configuration lives in `docs.json`
- Run `mint dev` to preview locally on port 3000
- Run `mint broken-links` to check links
- Run `make lint` for the full validation bundle (schema, broken links, markdown link check)
- Deploys automatically on push to the default branch (Mintlify GitHub integration)

## Terminology

- Use "agent" (lowercase) for the product noun — the always-on agent process. "agent" is legacy terminology; do not use it in new prose (brand/code tokens like `agentsfleet`, `agentsfleet`, `agentsfleetd`, `zmb_`, `agent_id`, and `/agents/` paths stay)
- Use "workspace" not "project"
- Use "skill" for a named capability an agent can invoke (agentmail, slack, github, ...)
- Use "trigger" for how an agent receives events (today: webhook)
- Use "credential firewall" for the network-layer proxy that injects secrets outside the sandbox
- Use "activity stream" not "logs" or "audit log" for the append-only event record
- Use "kill switch" for the immediate stop mechanism
- Use "event" not "job" for a single webhook delivery; the agent's work on one event is a "run"
- Use "run" for one end-to-end execution of the agent on one trigger — formerly "stage"
- Use "execution" only as the general noun (e.g. "hosted execution"), not for the discrete unit
- Use "runner" for the execution-plane process that sandboxes and runs an agent — not "executor"
- Use "agent" not "bot" or "AI"
- Use "PR" not "pull request" (except on first mention per page)
- Use `agentsfleet` in code formatting when referring to CLI commands
- Use `agentsfleetd` in code formatting when referring to server processes
- Use "Dashboard" (capitalized in headings, lowercase "dashboard" in body prose) for the web app at `app.agentsfleet.net`. The earlier aspirational name for this surface is retired — do not reintroduce it.

Forbidden terminology: `spec`, `stage`, `gate loop`, `scorecard`. These refer to a v1 product surface that has been removed. Do not introduce them into new pages. (`run`/`runs` are now the v2 execution unit — see Terminology above.)

## Style preferences

- Use active voice and second person ("you")
- Keep sentences concise — one idea per sentence
- Use sentence case for headings
- Bold for UI elements: Click **Settings**
- Code formatting for file names, commands, paths, and code references
- Mermaid for all sequence and architecture diagrams
- Do not use time estimates or effort ratings in user-facing docs
- Mark future features with `<Note>` callout: "This feature is coming soon."

## Content boundaries

- Do not document internal deployment playbooks (those live in the main repo)
- Do not expose credential values, vault paths, or 1Password references
- Do not document internal agent pipeline internals (NullClaw config details, runner RPC protocol) — keep operator docs at the operational level
- Do not reference specific cloud provider pricing or account details

## When closing out a feature PR in the lead repo (companion docs flow)

A landing PR in any lead repo (`agentsfleet`, `agentsfleet`, the website, the app) almost always drifts the docs site. Before the lead-repo PR flips ready-for-review:

1. **Review the lead PR's changed files.** Every public-surface change is a candidate doc edit — HTTP request/response shape, CLI subcommand or flag, frontmatter schema, error code, env var, default value, response field, pricing / billing copy, dashboard flow.
2. **Identify the `.mdx` pages that drift.** Grep this docs repo for the old field name, old YAML shape, old subcommand, old copy. Common candidates: `quickstart.mdx`, `cli/*.mdx`, `agents/*.mdx` (especially `authoring.mdx`, `webhooks.mdx`, `install.mdx`, `running.mdx`), `api-reference/*.mdx`, `billing/*.mdx`, `snippets/rates.mdx`, `concepts/*.mdx`.
3. **Update the relevant pages.** Fix examples, tables, and prose. Preserve load-bearing detail (`UZ-XXX-NNN` error codes, endpoint paths, env var names, schema column names, money amounts). Don't rewrite past entries; only touch pages that no longer describe what shipped.
4. **Add a `changelog.mdx` `<Update>` block** at the top, after the leading `<Tip>`. Section order is fixed: Upgrading → What's new → API reference → Bug fixes → CLI. Voice rules: lead with the change, no marketing words, no milestone IDs / spec filenames / `RULE XXX` references. Date label `MMM DD, YYYY`, no semver prefix. Two entries on the same date get distinct titles (no disambiguator suffix needed) or a merged block.
5. **All four steps land on a dedicated docs-repo branch** — `chore/m{N}-{slug}-changelog` off `main`. Do not commit docs changes on the lead-repo feature branch (it's a separate repository) and do not commit on `main` directly. Open the docs PR alongside the lead PR so reviewers can cross-link the two.

The rule applies to every milestone PR, not just trigger/CLI ones — schema migrations, new endpoints, deprecations, billing changes, dashboard rewrites all drift docs.

## Design system colors

Mirror `ui/packages/design-system/src/tokens.css` from the matching product branch when changing `docs.json` or `style.css`.

- Page: `#131d21` dark / `#f7faf9` light.
- Surfaces: `#1c292e`, `#26363d`, `#31434c` dark / `#ffffff`, `#edf3f1`, `#dfe9e5` light.
- Text: `#f1f5f5` dark / `#14251f` light. Secondary: `#c6d2d5` / `#435d52`.
- Links and selected navigation: `#5eead4` dark / `#087568` light.
- Primary action: mint with dark text in dark mode; ink with white text in light mode.
- Typography: Bricolage Grotesque page titles, Instrument Sans reading and interface text, Commit Mono code and technical values.
- Use flat fills and readable contrast. Keep the shipped fonts local; preserve their licenses.
