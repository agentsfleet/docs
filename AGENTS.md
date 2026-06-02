# Documentation project instructions

## About this project

- This is the usezombie documentation site built on [Mintlify](https://mintlify.com)
- Pages are MDX files with YAML frontmatter
- Configuration lives in `docs.json`
- Run `mint dev` to preview locally on port 3000
- Run `mint broken-links` to check links
- Run `make lint` for the full validation bundle (schema, broken links, markdown link check)
- Deploys automatically on push to the default branch (Mintlify GitHub integration)

## Terminology

- Use "zombie" (lowercase) for the product noun — the always-on agent process
- Use "workspace" not "project"
- Use "skill" for a named capability a zombie's agent can invoke (agentmail, slack, github, ...)
- Use "trigger" for how a zombie receives events (today: webhook)
- Use "credential firewall" for the network-layer proxy that injects secrets outside the sandbox
- Use "activity stream" not "logs" or "audit log" for the append-only event record
- Use "kill switch" for the immediate stop mechanism
- Use "event" not "job" for a single webhook delivery; the agent's work on one event is a "run"
- Use "run" for one end-to-end execution of the agent on one trigger — formerly "stage"
- Use "execution" only as the general noun (e.g. "hosted execution"), not for the discrete unit
- Use "runner" for the execution-plane process that sandboxes and runs a zombie's agent — not "executor"
- Use "agent" not "bot" or "AI"
- Use "PR" not "pull request" (except on first mention per page)
- Use `zombiectl` in code formatting when referring to CLI commands
- Use `zombied` in code formatting when referring to server processes
- Use "Dashboard" (capitalized in headings, lowercase "dashboard" in body prose) for the web app at `app.usezombie.com`. The earlier aspirational name for this surface is retired — do not reintroduce it.

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

A landing PR in any lead repo (`usezombie`, `zombiectl`, the website, the app) almost always drifts the docs site. Before the lead-repo PR flips ready-for-review:

1. **Review the lead PR's changed files.** Every public-surface change is a candidate doc edit — HTTP request/response shape, CLI subcommand or flag, frontmatter schema, error code, env var, default value, response field, pricing / billing copy, dashboard flow.
2. **Identify the `.mdx` pages that drift.** Grep this docs repo for the old field name, old YAML shape, old subcommand, old copy. Common candidates: `quickstart.mdx`, `cli/*.mdx`, `zombies/*.mdx` (especially `authoring.mdx`, `webhooks.mdx`, `install.mdx`, `running.mdx`), `api-reference/*.mdx`, `billing/*.mdx`, `snippets/rates.mdx`, `concepts/*.mdx`.
3. **Update the relevant pages.** Fix examples, tables, and prose. Preserve load-bearing detail (`UZ-XXX-NNN` error codes, endpoint paths, env var names, schema column names, money amounts). Don't rewrite past entries; only touch pages that no longer describe what shipped.
4. **Add a `changelog.mdx` `<Update>` block** at the top, after the leading `<Tip>`. Section order is fixed: Upgrading → What's new → API reference → Bug fixes → CLI. Voice rules: lead with the change, no marketing words, no milestone IDs / spec filenames / `RULE XXX` references. Date label `MMM DD, YYYY`, no semver prefix. Two entries on the same date get distinct titles (no disambiguator suffix needed) or a merged block.
5. **All four steps land on a dedicated docs-repo branch** — `chore/m{N}-{slug}-changelog` off `main`. Do not commit docs changes on the lead-repo feature branch (it's a separate repository) and do not commit on `main` directly. Open the docs PR alongside the lead PR so reviewers can cross-link the two.

The rule applies to every milestone PR, not just trigger/CLI ones — schema migrations, new endpoints, deprecations, billing changes, dashboard rewrites all drift docs.

## Design system colors

{/* SYNC SOURCE: ~/Projects/usezombie/ui/packages/design-system/src/tokens.css
     When touching colors in this repo (docs.json, logos, custom CSS), always
     verify values against the canonical design-system tokens first.
     Run: grep -E "^  --(pulse|bg|surface|text|success|warn|error|info|evidence)" ~/Projects/usezombie/ui/packages/design-system/src/tokens.css

     Heritage `--z-orange` palette retired in M64 (Operational Restraint
     rollout). Anything still referencing `#d96b2b` / `--z-orange` is stale. */}

The accent is currency, never decoration: cyan-mint pulse appears only on live signals (running zombies, focus rings, primary CTAs, the brand-mark). Everything else is muted/subtle/info/warn/error/evidence.

Primary brand accent (the wake-pulse): `#5eead4` (`--pulse`, dark mode), `#14b8a6` (`--pulse`, light mode).
Pulse glow ring: `rgba(94, 234, 212, 0.35)` (`--pulse-glow`).
Background dark: `#0a0d0e` (`--bg`). Surface: `#11161a` (`--surface-1`).
Background light: `#f8f6f1` (`--bg`, parchment-warm). Surface: `#f1eee6` (`--surface-1`).
Text primary: `#e6eaec` (`--text`, dark) / `#1a1d1e` (`--text`, light). Text muted: `#8b9398` / `#5a625f`.
Status colors: success `#34d399` (`--success`), warn `#f59e0b` (`--warn`), error `#f87171` (`--error`), info `#60a5fa` (`--info`), evidence `#fbbf24` (`--evidence`, cited evidence callouts only).
Typography: Commit Mono (`--ff-mono`) for headings + code; Instrument Sans Variable (`--ff-sans`) for body.
