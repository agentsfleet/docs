# MDX

This standard covers Markdown JSX (MDX) pages as a language: front matter, component nesting, expressions in prose, code fences, links and image descriptions.
A coding agent reads it before editing a `*.mdx` file, and a reviewer judges a diff against it.
Prose style belongs to the documentation standards, and renderer-specific rules belong to that renderer's own pack.

## Syntax

### MDX-FRONT — Front matter parses as YAML and carries every key the site's renderer requires.
- **Applies to:** `**/*.mdx`
- **Checked by:** review
- **Bad:** `title: Projects: the overview`
- **Good:** `title: "Projects: the overview"`
- **Why:** a second unquoted colon is a YAML error, so the page fails the build or renders without its title.

### MDX-NEST — JSX components close in the reverse order they open, and every component a page uses is imported or provided by the site.
- **Applies to:** `**/*.mdx`
- **Checked by:** review
- **Bad:** `<Steps><Step title="Install">…</Steps></Step>`
- **Good:** `<Steps><Step title="Install">…</Step></Steps>`
- **Why:** MDX compiles JSX strictly, so one misnested tag or unknown component breaks the page.

### MDX-EXPR — Braces and angle brackets in prose sit inside inline code, because MDX reads them as expressions and JSX.
- **Applies to:** `**/*.mdx`
- **Checked by:** review
- **Bad:** `Call /projects/{project_id} with a <token> header.`
- **Good:** ``Call `/projects/{project_id}` with a `<token>` header.``
- **Why:** an unwrapped `{project_id}` runs as JavaScript and an unclosed `<token>` is read as a tag, so the page fails to build or render.

### MDX-FENCE — A code fence names its language and closes with a fence of the same character and at least the same length.
- **Applies to:** `**/*.mdx`
- **Checked by:** review
- **Bad:** a fence opened with three backticks and no language, and never closed
- **Good:** a fence opened with three backticks and `bash`, and closed with three backticks
- **Why:** an unclosed fence swallows the rest of the page as code, and a fence with no language loses its highlighting.

## Links and images

### MDX-LINK — Every internal link resolves to a page or heading anchor in the same build.
- **Applies to:** `**/*.mdx`
- **Checked by:** review
- **Bad:** a link to `/project/overview` while the page lives at `projects/overview.mdx`
- **Good:** a link to `/projects/overview`, matching the page path
- **Why:** a broken internal link renders fine and fails only when a reader clicks it.

### MDX-ALT — Every image carries alt text that says what it shows, and a decorative image carries an explicit empty `alt`.
- **Applies to:** `**/*.mdx`
- **Checked by:** review
- **Bad:** `<img src="/images/project-list.png" />`
- **Good:** `<img src="/images/project-list.png" alt="Project list with two active projects" />`
- **Why:** a screen reader announces a missing alt as the file name, and the image's meaning never reaches that reader.

## Renderer scope

### MDX-MINTLIFY — Mintlify-specific rules apply only to a repository that builds with Mintlify.
- **Applies to:** `**/*.mdx`
- **Checked by:** review
- **Bad:** flagging a missing `docs.json` navigation entry in an MDX repository built with another renderer
- **Good:** Mintlify components and `docs.json` checks where the repository builds with Mintlify, and only the generic rules here elsewhere
- **Why:** a rule written for one renderer's components fails pages that are correct for another.
