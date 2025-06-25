import requests
import fitz
from llm.router_llm import call_llm

def summarize_content(pdf_url: str) -> dict:
    response = requests.get(pdf_url)
    with open("temp.pdf" , "wb") as f:
        f.write(response.content)

    text = ""
    with fitz.open("temp.pdf") as doc:
        for page in doc:
            text += page.get_text()
            if len(text) > 5000:
                break

    prompt = f"Summarize the research paper:\n{text[:5000]}:"
    summary = call_llm(prompt)
    return {"summary":summary}
    