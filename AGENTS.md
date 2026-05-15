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
- Use "event" not "run" or "job" for a single webhook delivery processed by a zombie
- Use "execution" for the billable per-event agent reasoning window
- Use "agent" not "bot" or "AI"
- Use "PR" not "pull request" (except on first mention per page)
- Use `zombiectl` in code formatting when referring to CLI commands
- Use `zombied` in code formatting when referring to server processes
- Use "Dashboard" (capitalized in headings, lowercase "dashboard" in body prose) for the web app at `app.usezombie.com`. The earlier aspirational name for this surface is retired — do not reintroduce it.

Forbidden terminology: `spec`, `run`, `runs`, `gate loop`, `scorecard`. These refer to a v1 product surface that has been removed. Do not introduce them into new pages.

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
- Do not document internal agent pipeline internals (NullClaw config details, executor RPC protocol) — keep operator docs at the operational level
- Do not reference specific cloud provider pricing or account details

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
