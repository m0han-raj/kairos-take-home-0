from mcp_servers.search_paper import search_for_paper
from mcp_servers.summarize import summarize_content

def run_agent(query):
    papers = search_for_paper(query)
    
    if not papers:
        yield {"tool_output": [{
            "title": "No papers found",
            "pdf_link": "",
            "summary": f"Sorry, I couldn't find any papers matching your query: '{query}'."
        }]}
        return

    results = []
    for paper in papers:
        if not paper.get("pdf_link"):
            summary_text = "No PDF link available to generate a summary."
        else:
            summary = summarize_content(paper["pdf_link"])
            summary_text = summary.get("summary", "Failed to generate summary.")
        
        results.append({
            "title": paper.get("title", "No Title"),
            "pdf_link": paper.get("pdf_link", ""),
            "summary": summary_text
        })
        
    yield {"tool_output": results}
