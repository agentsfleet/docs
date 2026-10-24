<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="logo/dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="logo/light.svg" />
  <img src="logo/dark.svg" width="200" alt="agentsfleet" />
</picture>

**Documentation for agentsfleet.**

`agentsfleet` runs fleets that respond to webhooks, schedules, and messages.
You review each fleet's tools, access, and spending limits before saving it.
Use these docs to create fleets, inspect runs in the activity stream, and manage your workspace.

[![Docs](https://img.shields.io/badge/agentsfleet-Docs-B8F0CE?style=for-the-badge)](https://docs.agentsfleet.net)
[![Get early access](https://img.shields.io/badge/agentsfleet-Get_early_access-B8F0CE?style=for-the-badge)](https://accounts.agentsfleet.net/waitlist)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

</div>

---

## Development

Before editing, read `AGENTS.md` and this repository's `.orly/dispatch/write_documentation.md`. For changelog edits, also read `.orly/docs/CHANGELOG_VOICE.md`.

1. Use Bun 1.4.3 and Node.js 24, then install the pinned documentation tools. Mintlify starts a Node.js process for its CLI.

```bash
bun install --frozen-lockfile
```

```text
bun install v1.4.3 (<varies>)
<varies>
```

2. Enable the repository's pre-commit checks.

```bash
make install-hooks
```

```text
Git hooks enabled from .githooks
```

3. Start the local preview.

```bash
make dev
```

```text
Local: http://localhost:3000
```

View your local preview at `http://localhost:3000`.

4. Check changed prose, page metadata, site configuration, and links before pushing.

```bash
bun run orly gate verify
```

```text
🔆 gate verify
  🟢 repo.config: <varies>
  🟢 docs.language: <varies>
  🟢 cmd.verify.docs: <varies>
```

Orly 0.17.0 keeps the writing rules in this checkout. Reinstall dependencies after cloning; `make install-hooks` enables checks at commit and push.

## Publishing

The [Mintlify GitHub app](https://dashboard.mintlify.com/settings/organization/github-app) deploys every change pushed to the default branch.

## License

MIT — Copyright (c) 2026 agentsfleet
