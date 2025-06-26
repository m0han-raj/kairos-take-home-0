import requests
import fitz  # PyMuPDF
import os
import tempfile
import logging
from llm.router_llm import call_llm

def summarize_content(pdf_url: str) -> dict:
    if not pdf_url:
        return {"summary": "No PDF URL provided."}

    try:
        response = requests.get(pdf_url, timeout=20)
        response.raise_for_status()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            temp_pdf.write(response.content)
            temp_pdf_path = temp_pdf.name

        text = ""
        try:
            with fitz.open(temp_pdf_path) as doc:
                # Extract text from the entire document for a more comprehensive summary
                for page in doc:
                    text += page.get_text()
        finally:
            os.remove(temp_pdf_path)

        if not text.strip():
            return {"summary": "Could not extract text from the PDF."}

        prompt = (
            "You are a research assistant. Please provide a concise, easy-to-understand summary "
            "of the following research paper abstract or introduction. Focus on the key findings and implications.\n\n"
            f"Paper Content:\n'''\n{text[:8000]}\n'''\n\n"
            "Summary:"
        )

        summary = call_llm(prompt)

        if not summary or summary.strip().lower() == 'none':
            return {"summary": "The language model could not generate a summary."}

        return {"summary": summary}

    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to download PDF from {pdf_url}: {e}")
        return {"summary": f"Error: Could not download the PDF file."}
    except fitz.fitz.FitzError as e:
        logging.error(f"Failed to process PDF from {pdf_url}: {e}")
        return {"summary": "Error: The document is not a valid or readable PDF."}
    except Exception as e:
        logging.exception(f"An unexpected error occurred while summarizing {pdf_url}")
        return {"summary": "An unexpected error occurred during summarization."}
