import ollama

# Example: Summarize a paragraph of text
text = """
OpenAI has introduced a new tool called Ollama that lets users run large language models on local machines.
This approach emphasizes privacy and control, as data does not leave the user's environment.
Developers can leverage various open-source models through a simple interface, improving efficiency and reducing costs.
"""
prompt = f"Summarize the following text in one sentence:\n\"\"\"\n{text}\n\"\"\""
result = ollama.generate(model='phi', prompt=prompt)
print("Summary:", result['response'])