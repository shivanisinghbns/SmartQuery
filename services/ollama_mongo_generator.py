import ollama
import json

def build_prompt(question):
    return f"""
You are a MongoDB query builder assistant.

Your job is to extract:
1. The relevant MongoDB collection(s) mentioned in the user's question.
2. Any filters such as timestamp, status_code, or category.

You must follow these rules:
- Use only the following valid collections: "coal", "water", "local", "environment"
- If no valid collection is mentioned, return: "collections": []
- If no filters are applicable, return an empty object: "filter": {{}}
- The timestamp format must be YYYY-MM-DD
- Do not include fields like status_code or category unless explicitly asked
- Respond with valid JSON only — no text, no explanation, no markdown

Expected format:
{{
  "collections": [],
  "filter": {{
    "timestamp": {{
      "after": ""
    }}
  }}
}}

User question: "{question}"

Respond with JSON only.
"""


def extract_json(text):
    try:
        start = text.index('{')
        end = text.rindex('}') + 1
        return json.loads(text[start:end])
    except Exception as e:
        print("Error extracting JSON:", e)
        return {}

def get_collections_from_prompt(question):
    prompt = build_prompt(question)

    try:
        result = ollama.generate(model='mistral', prompt=prompt)
        print(result['response'])
        response_text = result.get("response", "")
        parsed = extract_json(response_text)

        collections = parsed.get("collections", [])
        filters = parsed.get("filter", {})
        return collections, filters

    except Exception as e:
        print("Ollama error:", e)
        return [], {}


