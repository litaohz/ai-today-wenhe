---
name: html-2-screenshot
description: Capture screenshots from local or served HTML pages, especially when asked to open a browser and take one-block-at-a-time screenshots for sharing or social posts.
---

# HTML to Screenshots

Use the browser agent to open the target HTML (local file or URL) and capture screenshots section by section.

## Workflow

1. **Setup**:
   - Set viewport size to **Width: 600px, Height: 1600px** (Increased range).
   - **Remove Blue Focus Rings**: Inject CSS `* { outline: none !important; box-shadow: none !important; }` to prevent blue glows around active elements.
   - Open the target HTML (local file or URL).

2. **Capture Sequence**:
   - **01. Header & Overview**: Capture the `.header` and `.overview-card` together as a single image (combine them if necessary).
   - **02...N. Details**: Capture each `.detail-card` individually.
   - **99. Footer**: Capture the `.footer`. **Critical**: Ensure the window height is fully expanded (e.g., resize to element height + 100px) to prevent cutting off content.

3. **Naming Convention**:
   - `summary_01_header_overview.png`
   - `summary_02_detail_1.png`
   - `summary_03_detail_2.png`
   - ...
   - `summary_99_footer.png`

## Notes

- **Blue Light Fix**: The CSS injection is crucial to avoid "blue light" selection halos.
- **Inclusion over Exclusion**: Ensure padding/margins are included for a clean look.
- **Verification**: Always check if standard DOM retrieval fails; if so, apply the "Make Interactive" fix immediately.
