import os

def call_llm(prompt: str) -> str:
    provider = os.getenv("LLM_PROVIDER")
    model_name = os.getenv("LLM_MODEL")

    if provider == "gemini":
        import google.generativeai as genai
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        return response.text.strip()

    elif provider == "openai":
        import openai
        openai.api_key = os.getenv("OPENAI_API_KEY")
        response = openai.ChatCompletion.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()

    elif provider == "anthropic":
        import anthropic
        client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        response = client.messages.create(
            model=model_name,
            max_tokens=1024,
            temperature=0.7,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text.strip()

    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")
