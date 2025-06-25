from mcp_servers.search_paper import search_for_paper
from mcp_servers.summarize import summarize_content 
from datetime import datetime

def run_agent(query):
    timestamp = datetime.now().isoformat()
    papers = search_for_paper(query)

    for paper in papers:
        summary = summarize_content(papers[0]["pdf_link"])
        print(f"Paper: {paper['title']}\nSummary: {summary['summary']}\n")
