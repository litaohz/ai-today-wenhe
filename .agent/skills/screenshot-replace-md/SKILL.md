---
name: screenshot-replace-md
description: Create a copy of a Markdown file and replace URLs in the copy with screenshots by using a GUI browser agent. Especially for X/Twitter posts; use when a user asks to open links from an md file and swap them for image screenshots, with Chinese translation visible and minimal cropping of core content.
---

# Screenshot Replace for Markdown

## Goal

Create a copy of a Markdown file and replace one or more URLs in the copy with local image screenshots captured via a GUI browser agent.

## Workflow

1. Create a directory named `archives-<YYMMDD>` using the current date (e.g., `archives-260116` for Jan 16, 2026) if it does not already exist.
2. Copy the target Markdown file into this `archives-<YYMMDD>` directory, appending `-screenshot` to the filename (e.g., `archives-260116/filename-screenshot.md`) to preserve the original.
3. Open the **new** copy of the Markdown file and identify every URL to replace.
4. For each URL, use the GUI agent to navigate to the page.
5. Wait 3 seconds for the page to fully load.
6. Ensure Chinese translation is visible for the main content.
   - Use the page's translate control if available.
   - Wait until the translated text appears before capturing.
7. Take a minimal, content-only screenshot (element or tight crop).
8. Save the screenshot with a descriptive name inside the `archives-<YYMMDD>` directory.
9. Replace the URL in the **new** Markdown copy with a Markdown image link to the screenshot (relative path).

## X/Twitter Screenshot Rules

When the URL is a tweet or X/Twitter post, capture only the tweet container:

- Include: author info (profile pic, name, handle), tweet text, media (if any), engagement metrics.
- Exclude: left navigation, right sidebar/search, and anything below metrics (replies/comments).
- Prefer an element screenshot of the main tweet article element.

## Replacement Format

Use Markdown image syntax and keep paths relative to the Markdown file when possible:

```
![descriptive-alt-text](./path/to/screenshot.png)
```

## File Naming

Use a descriptive, stable filename based on author and content, for example:

```
author-handle-keywords.png
```

## Quality Checks

- Translation is visible in the captured area.
- Screenshot is tight and focused on core content only.
- No UI chrome, sidebars, or replies included.
