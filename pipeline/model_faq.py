import os
import json
from dotenv import load_dotenv
from groq import Groq

from .schemas import FAQResponse

load_dotenv()

def _build_prompt(clean_text: str, url: str) -> str:
    return f"""
You are an information extraction system.

Task: From the website content below, extract FAQ-style question/answer pairs.

Rules:
- Use ONLY the provided content. Do NOT invent facts.
- If the content does not support good Q/A, return an empty list.
- Answers must be short, clear, and user-friendly.
- Group each Q/A under a theme (e.g., Shipping, Returns, Pricing, Account, Support, Security, etc.)
- Output MUST be valid JSON only (no markdown, no commentary).

Output JSON schema EXACTLY:
{{
  "url": "{url}",
  "items": [
    {{
      "theme": "string",
      "question": "string",
      "answer": "string",
      "confidence": 0.0
    }}
  ]
}}

Website content:
\"\"\"{clean_text}\"\"\"
""".strip()

def extract_faq_with_model(clean_text: str, url: str) -> FAQResponse:
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("Missing GROQ_API_KEY. Put it in .env")

    client = Groq(api_key=api_key)
    prompt = _build_prompt(clean_text=clean_text, url=url)

    # IMPORTANT: ask Groq to return strict JSON
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You must output ONLY valid JSON. No markdown. No commentary."},
            {"role": "user", "content": prompt},
        ],
        response_format={"type": "json_object"},
        temperature=0.2,
    )

    raw = (completion.choices[0].message.content or "").strip()

    # Parse JSON safely
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        # If something weird happens, fail gracefully instead of 500
        data = {"url": url, "items": []}

    if not data.get("url"):
        data["url"] = url

    return FAQResponse.model_validate(data)
