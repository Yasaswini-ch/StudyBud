"""
Thin, provider-agnostic wrapper so the app can talk to OpenAI, Groq, or
Gemini with the same function call. Groq exposes an OpenAI-compatible
endpoint, so it reuses the `openai` client with a different base_url.
"""

from openai import OpenAI

PROVIDERS = {
    "OpenAI": {"default_model": "gpt-4o-mini", "base_url": None},
    "Groq": {"default_model": "llama-3.3-70b-versatile", "base_url": "https://api.groq.com/openai/v1"},
    "Gemini": {"default_model": "gemini-1.5-flash", "base_url": None},
}


def chat(provider: str, api_key: str, model: str, system_prompt: str, history: list, user_prompt: str) -> str:
    """history is a list of (role, content) tuples with role in {"user", "assistant"}."""
    if provider in ("OpenAI", "Groq"):
        base_url = PROVIDERS[provider]["base_url"]
        client = OpenAI(api_key=api_key, base_url=base_url)
        messages = [{"role": "system", "content": system_prompt}]
        messages += [{"role": role, "content": content} for role, content in history]
        messages.append({"role": "user", "content": user_prompt})
        response = client.chat.completions.create(model=model, messages=messages, temperature=0.7)
        return response.choices[0].message.content

    if provider == "Gemini":
        import google.generativeai as genai

        genai.configure(api_key=api_key)
        gemini_model = genai.GenerativeModel(model, system_instruction=system_prompt)
        gemini_history = [
            {"role": "model" if role == "assistant" else "user", "parts": [content]}
            for role, content in history
        ]
        session = gemini_model.start_chat(history=gemini_history)
        response = session.send_message(user_prompt)
        return response.text

    raise ValueError(f"Unknown provider: {provider}")
