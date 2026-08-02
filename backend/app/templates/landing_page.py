LANDING_PAGE_TEMPLATE = """
Generate a complete responsive HTML5 landing page.

Requirements:

- Modern UI
- Embedded CSS
- No external libraries
- Mobile responsive
- Professional design
- Complete HTML document

IMPORTANT

Return ONLY valid JSON.

Schema:

{
  "title": "Landing Page",
  "type": "html",
  "content": "<!DOCTYPE html>...</html>"
}

Rules:

- The "content" field must contain the ENTIRE HTML document.
- Escape all quotes inside the HTML so the JSON remains valid.
- Do NOT wrap the JSON inside markdown.
- Do NOT explain anything.
- Return ONLY the JSON object.
"""