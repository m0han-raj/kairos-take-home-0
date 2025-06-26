import requests
import xml.etree.ElementTree as ET
import logging

def search_for_paper(query: str, max_results: int = 5):
    base_url = "http://export.arxiv.org/api/query"
    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": max_results
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status() 
        
        root = ET.fromstring(response.content)
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        papers = []

        for entry in root.findall("atom:entry", ns):
            title_element = entry.find("atom:title", ns)
            pdf_link_element = entry.find("atom:link[@type='application/pdf']", ns)

            if title_element is not None and pdf_link_element is not None:
                papers.append({
                    "title": title_element.text.strip() if title_element.text else "No Title",
                    "pdf_link": pdf_link_element.get("href", "").strip()
                })
        return papers

    except requests.exceptions.ConnectionError as e:
        logging.error(f"Failed to connect to arXiv: {e}")
        return []
    except requests.exceptions.Timeout as e:
        logging.error(f"Timeout occurred while fetching papers from arXiv: {e}")
        return []
    except requests.exceptions.HTTPError as e:
        logging.error(f"HTTP error occurred while fetching papers from arXiv: {e}")
        return []
    except requests.exceptions.RequestException as e:
        logging.error(f"An unexpected error occurred while fetching papers from arXiv: {e}")
        return []
    except ET.ParseError as e:
        logging.error(f"Failed to parse arXiv response: {e}")
        return []