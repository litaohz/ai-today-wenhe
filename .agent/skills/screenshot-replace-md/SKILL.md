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


26: ## X/Twitter Smart Capture Rules
27: 
28: When the URL is a tweet or X/Twitter profile link:
29: 
30: ### 1. Topic Verification (Smart Check)
31: - **Do NOT** blindly capture the first tweet if it is a "Pinned" tweet.
32: - **Check specific keywords**: Ensure the tweet text matches the keywords or topic from the summary (e.g., if the summary mentions "Veo", the tweet MUST contain "Veo").
33: - **Scroll if needed**: If the first tweet is pinned and irrelevant (e.g., an old feature announcement), scroll down to find the *actual* news tweet.
34: - **Expand text**: Click "Show more" if the key content is truncated.
35: 
36: ### 2. Visual Composition
37: - **Include**: Author info (profile pic, name, handle), full tweet text, media (if any), engagement metrics.
38: - **Exclude**: Left navigation, right sidebar/search, and replies/comments below the metrics.
39: - **Target**: Identify the `<article>` element corresponding to the correct tweet and capture that element specifically.
40: 
41: ## Replacement Format
42: 
43: Use Markdown image syntax and keep paths relative to the Markdown file when possible:
44: 
45: ```
46: ![descriptive-alt-text](./path/to/screenshot.png)
47: ```
48: 
49: ## File Naming
50: 
51: Use a descriptive, stable filename based on author and content, for example:
52: 
53: ```
54: author-handle-keywords.png
55: ```
56: 
57: ## Quality Checks
58: 
59: - **Relevance**: Does the screenshot actually match the news item description?
60: - **Translation**: Is Chinese translation visible (if requested/available)?
61: - **Focus**: Is the screenshot tight and focused on the core content without UI chrome?

