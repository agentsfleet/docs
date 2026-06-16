#!/usr/bin/env bash
# M51_001 docs-site test specification — see
# agentsfleet/agentsfleet:docs/v2/active/M51_001_*.md §Test Specification.
#
# Source-file checks. Mintlify "renders" iff the source file exists with
# required content; "404s" iff the source file is absent (or hidden via
# .mintignore). The cross-tab API drift check is wired separately in
# `make _lint-openapi-drift`.

set -euo pipefail

cd "$(dirname "$0")/.."

fail=0
pass=0

check() {
  local name="$1"
  local cmd="$2"
  if eval "$cmd" >/dev/null 2>&1; then
    printf "  ✓ %s\n" "$name"
    pass=$((pass + 1))
  else
    printf "  ✗ %s\n" "$name"
    fail=$((fail + 1))
  fi
}

echo "M51_001 docs-site spec tests"

check "test_quickstart_page_renders" \
  '[ -f quickstart.mdx ] && grep -q "platform-ops" quickstart.mdx && grep -q "agentsfleet-install-platform-ops" quickstart.mdx'

check "test_concepts_context_lifecycle_renders" \
  '[ -f concepts/context-lifecycle.mdx ] && grep -q "tool_window" concepts/context-lifecycle.mdx && grep -q "memory_checkpoint_every" concepts/context-lifecycle.mdx'

check "test_skills_index_renders" \
  '[ -f skills/index.mdx ] && grep -q "agentsfleet-install-platform-ops" skills/index.mdx'

check "test_concepts_v2_rewritten" \
  '! grep -E -i "AI-generated PRs|automated PR delivery|validated pull request" concepts.mdx'

check "test_how_it_works_deleted" \
  '[ ! -f how-it-works.mdx ]'

check "test_no_self_host_page_in_v2" \
  '[ ! -f self-host.mdx ]'

# Operator/ directory removed entirely (v1 self-host content was stale; v3 docs
# will be authored fresh from agentsfleet/agentsfleet:docs/architecture/). Source
# absent → every /operator/* URL 404s.
check "test_no_operator_pages_render" \
  '[ ! -d operator ]'

check "test_no_privacy_telemetry_page_in_v2" \
  '[ ! -f privacy/cli-telemetry.mdx ]'

check "test_homelab_pages_404" \
  '[ ! -f integrations/lead-collector.mdx ] && [ ! -f launch/homelab-agent.mdx ]'

# Cross-tab API entry resolution. Each `<METHOD> /<path>` entry in docs.json's
# "API reference" tab must exist in the upstream openapi.json. Defers to the
# Makefile target which fetches and diffs against the live spec.
check "test_api_tab_routes_resolve_in_openapi" \
  'make _lint-openapi-drift'

# ── Regression guards (M51_001 corrections) ─────────────────────────────────
#
# Each pins a real drift caught during the PR. A grep returning a non-historical
# hit means someone re-introduced framing the runtime no longer ships. The
# changelog/ directory is excluded — historical Update entries reflect the
# product as it was when the entry was written and are intentionally stale.

# v1 sample names. Only platform-ops ships in agentsfleet/agentsfleet:samples/.
# Re-introducing `slack-bug-fixer` or `homelab` in a current page sends
# operators down `agentsfleet install <name>` paths that fail with
# MISSING_ARGUMENT.
check "test_no_v1_sample_names_in_current_docs" \
  '! grep -rEl --include="*.mdx" --exclude-dir=changelog "slack-bug-fixer|slack_bug_fixer|\bhomelab\b|lead[_-]collector|lead[_-]scorer|homebox|pr-reviewer|pr_reviewer" . | grep -v "^./changelog.mdx$" | grep -q .'

# `agentsfleet up` does not exist in agentsfleet/src/program/routes.js. Install IS
# the deploy in v2. Re-introducing it in a user-visible page sends operators
# down a "command not found" rabbit hole.
check "test_no_agentsfleet_up_in_current_docs" \
  '! grep -rEl --include="*.mdx" "agentsfleet up\b" . | grep -v "^./changelog.mdx$" | grep -q .'

# Top-level CLI verb is `agentsfleet login`, not `agentsfleet auth login`. Verified
# against agentsfleet/src/program/routes.js (the `login` route entry).
check "test_no_agentsfleet_auth_login_in_current_docs" \
  '! grep -rEl --include="*.mdx" "agentsfleet auth login" . | grep -v "^./changelog.mdx$" | grep -q .'

# Webhook URL canonical form is api.agentsfleet.net, per agentsfleet/agentsfleet:
# samples/platform-ops/README.md and skills/agentsfleet-install-platform-ops/
# SKILL.md. Re-introducing hooks.agentsfleet.net sends webhooks to a domain that
# does not resolve.
check "test_webhook_url_canonical_subdomain" \
  '! grep -rE --include="*.mdx" "hooks\\.agentsfleet\\.com" . | grep -v "^./changelog.mdx" | grep -q .'

# Memory entries land in memory.memory_entries per schema/013_memory_entries.
# sql:29 in agentsfleet/agentsfleet. core.agent_memories never existed.
check "test_memory_table_canonical_name" \
  '! grep -rE --include="*.mdx" "core\\.agent_memories|agent_memories" . | grep -q .'

# Real credential CLI shape per agentsfleet/src/commands/agent_credential.js
# is `--data='<json>'` or `--data=@-` (stdin). Stale flags: `--value=`,
# `--api-token`, `--bot-token`, `--host` for credential add. Each would fail
# with parseFlags rejecting the unknown flag.
check "test_credential_add_uses_data_flag" \
  '! grep -rE --include="*.mdx" "credential add[^|]*--(value|api-token|bot-token|host)=" . | grep -v "^./changelog.mdx" | grep -q .'

# v1 noun-form bans per ~/Projects/docs/AGENTS.md:30. Verb usage of "run/runs"
# (e.g. "the runtime runs") is allowed; this guard catches the specific noun
# phrasings that recurred in this PR's history.
check "test_no_v1_noun_phrasings" \
  '! grep -rE --include="*.mdx" "(failed run\b|production-branch run\b|webhook-driven runs|cron runs the|future runs\b|running the spec)" . | grep -v "^./changelog.mdx" | grep -q .'

echo
echo "  $pass passed, $fail failed"
[ "$fail" -eq 0 ]
