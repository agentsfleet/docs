<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="logo/dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="logo/light.svg" />
  <img src="logo/dark.svg" width="200" alt="agentsfleet" />
</picture>

**A fleet of prebuilt AI teammates for recurring engineering work.**

Each one wakes on an event — a pull request, an incident, a deploy — investigates across your code, telemetry, and live control-plane state, opens a scenario-backed fix, and waits for human approval before it ships or drafts the customer reply. Runs against a durable, replayable log — posts evidenced answers, never chats.

[![Docs](https://img.shields.io/badge/agentsfleet-Docs-5EEAD4?style=for-the-badge)](https://docs.agentsfleet.net)
[![Get early access](https://img.shields.io/badge/agentsfleet-Get_early_access-5EEAD4?style=for-the-badge)](https://agentsfleet.net)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

</div>

---

## Development

Install the [Mintlify CLI](https://www.npmjs.com/package/mint) to preview documentation changes locally:

```bash
npm i -g mint
mint dev
```

View your local preview at `http://localhost:3000`.

## Publishing

Changes pushed to the default branch are deployed automatically via the [Mintlify GitHub app](https://dashboard.mintlify.com/settings/organization/github-app).

## License

MIT — Copyright (c) 2026 agentsfleet
