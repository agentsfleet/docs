# Contribute to the documentation

Read `AGENTS.md`, `.orly/standards/docs.md` and `.orly/standards/docs-pages.md` before editing. For changelog entries, also read `.orly/standards/changelog.md`.

## How to contribute

### Option 1: Edit directly on GitHub

1. Navigate to the page you want to edit
2. Click the "Edit this file" button (the pencil icon)
3. Make your changes and submit a pull request

### Option 2: Local development

1. Fork and clone this repository, then open the cloned repository's directory
2. Use Bun 1.4.4 and Node.js 24, then install the pinned tools: `bun install --frozen-lockfile`
3. Create a branch for your changes
4. Make changes
5. Run `make dev`
6. Preview your changes at `http://localhost:3000`
7. Run `bun run orly gate verify` to check prose, page metadata, site configuration, and links
8. Commit your changes and submit a PR

For setup commands and expected output, see [local development](README.md#development).

## Writing guidelines

- **Use active voice**: "Run the command" not "The command should be run"
- **Address the reader directly**: Use "you" instead of "the user"
- **Keep sentences concise**: Aim for one idea per sentence
- **Lead with the goal**: Start instructions with what the user wants to accomplish
- **Use consistent terminology**: Don't alternate between synonyms for the same concept
- **Include examples**: Show, don't just tell
