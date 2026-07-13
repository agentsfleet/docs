<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="logo/dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="logo/light.svg" />
  <img src="logo/dark.svg" width="200" alt="agentsfleet" />
</picture>

**A fleet of prebuilt AI teammates for recurring engineering work.**

Each one wakes on an event — a pull request, an incident, a deploy. It investigates across your code, telemetry, and live control-plane state, then opens a scenario-backed fix. It waits for human approval before it ships or drafts the customer reply. It runs against a durable, replayable log — posts evidenced answers, never chats.

[![Docs](https://img.shields.io/badge/agentsfleet-Docs-5EEAD4?style=for-the-badge)](https://docs.agentsfleet.net)
[![Get early access](https://img.shields.io/badge/agentsfleet-Get_early_access-5EEAD4?style=for-the-badge)](https://accounts.agentsfleet.net/waitlist)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

</div>

---

## Development

Before editing a page or API text, read `~/Projects/dotfiles/docs/DOCUMENTATION_RULES.md`.

1. Install the [Mintlify CLI](https://www.npmjs.com/package/mint).

```bash
npm i -g mint
```

```text
added <varies> packages in <varies>
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
mint dev
```

```text
Local: http://localhost:3000
```

View your local preview at `http://localhost:3000`.

## Publishing

The [Mintlify GitHub app](https://dashboard.mintlify.com/settings/organization/github-app) deploys every change pushed to the default branch.

## License

MIT — Copyright (c) 2026 agentsfleet
