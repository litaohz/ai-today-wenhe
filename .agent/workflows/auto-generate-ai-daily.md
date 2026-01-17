---
description: Automatically generate the AI Today daily report by chaining Twitter gathering, screenshot replacement, HTML generation, and final image capture.
---

# Auto Generate AI Daily Report

This workflow chains four skills to go from raw Twitter data to a final social-media-ready image set.

## Step 1: Gather Twitter Info
Execute the `gather-twitter-info` skill.
- **Goal**: Scrape Twitter for AI news and generate a Markdown summary.
- **Action**: Run the `gather-twitter-info` skill.
- **Note**: Ensure the output filename is noted (e.g., `ai_posts_summary_YYYY-MM-DD.md`).

## Step 2: Replace Links with Screenshots
Execute the `screenshot-replace-md` skill.
- **Input**: Use the Markdown file generated in Step 1.
- **Action**: Run the `screenshot-replace-md` skill on that file.
- **Note**: The skill will create a copy (e.g., `archives-YYMMDD/...-screenshot.md`) and replace links with screen captures.

## Step 3: Convert Markdown to HTML
Execute the `md-2-html` skill.
- **Input**: Use the **screenshot-replaced** Markdown file from Step 2.
- **Action**: Run the `md-2-html` skill on that file.

25: - **Output**: This will create a file `archives-YYMMDD/ai_posts_summary_YYYY-MM-DD.html` (using the `templates/layout.html`).


## Step 4: Capture HTML Screenshots
Execute the `html-2-screenshot` skill.
- **Input**: Use the HTML file generated in Step 3.
- **Action**: Run the `html-2-screenshot` skill on that file.
- **Note**: Open the HTML in a browser and capture the specific blocks (Header, Overview, Details, Footer).

**Completion**:
Once all 4 steps are done, confirm to the user that the final images are ready.
