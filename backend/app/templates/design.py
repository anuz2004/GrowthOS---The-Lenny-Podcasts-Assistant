DESIGN_TEMPLATE = """
Generate a Technical Design Document.

Include:

- Goals
- UI Design
- UX
- Components
- Flow
- Edge Cases

IMPORTANT

Return ONLY valid JSON.

Schema:

{
  "title": "Technical Design Document",
  "type": "markdown",
  "content": "# Design Document\\n..."
}

Rules:

- The content field must contain the COMPLETE markdown document.
- Escape newlines using \\n.
- Escape double quotes.
- Do NOT wrap the JSON inside markdown fences.
- Do NOT explain anything.
- Return ONLY the JSON object.
"""