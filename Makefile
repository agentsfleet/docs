SHELL := /bin/bash

.PHONY: dev install-hooks lint test _lint-openapi-drift

OPENAPI_URL ?= https://raw.githubusercontent.com/agentsfleet/agentsfleet/main/public/openapi.json

dev:
	npx mintlify dev

install-hooks:
	@git config core.hooksPath .githooks
	@echo "Git hooks enabled from .githooks"

test:
	@python3 scripts/test-documentation.py
	@python3 scripts/check-documentation.py .

lint: test _lint-openapi-drift
	npx mintlify validate
	npx mintlify broken-links
	find . -name "*.mdx" | xargs -I{} npx markdown-link-check --config .mlc-config.json {}

_lint-openapi-drift:
	@command -v jq >/dev/null 2>&1 || { echo "jq is required for the OpenAPI drift check"; exit 1; }
	@tmp=$$(mktemp); \
	if ! curl -sSfL --connect-timeout 5 --max-time 10 "$(OPENAPI_URL)" -o "$$tmp"; then \
		echo "could not fetch $(OPENAPI_URL) for the OpenAPI drift check"; \
		rm -f "$$tmp"; exit 1; \
	fi; \
	upstream=$$(jq -r '.paths | to_entries[] | . as $$p | $$p.value | keys[] | (ascii_upcase + " " + $$p.key)' "$$tmp" | sort -u); \
	referenced=$$(grep -hoE '"(GET|POST|PUT|DELETE|PATCH) /[^"]+"' docs.json api-reference/endpoint/*.mdx 2>/dev/null | tr -d '"' | sort -u); \
	missing=$$(comm -23 <(echo "$$referenced") <(echo "$$upstream")); \
	unlisted=$$(comm -13 <(echo "$$referenced") <(echo "$$upstream")); \
	rm -f "$$tmp"; \
	if [ -n "$$missing" ]; then \
		echo "❌ openapi drift: paths referenced by docs but missing from $(OPENAPI_URL):"; \
		echo "$$missing" | sed 's/^/  - /'; \
		exit 1; \
	fi; \
	if [ -n "$$unlisted" ]; then \
		echo "❌ openapi drift: operations missing from docs.json:"; \
		echo "$$unlisted" | sed 's/^/  - /'; \
		exit 1; \
	fi; \
	echo "✓ openapi drift check clean"
