from mcp_servers.search_paper import search_for_paper
from mcp_servers.summarize import summarize_content 
from utils.logger import log_tool
from datetime import datetime

def run_agent(query):
    timestamp = datetime.now().isoformat()
    papers = search_for_paper(query)
    log_tool("search_for_paper", {"query": query}, papers, timestamp)

    for paper in papers:
        summary = summarize_content(paper["pdf_url"])
        log_tool("summarize_content", {"pdf_url": paper["pdf_url"]}, summary, timestamp)
        print(f"Paper: {paper['title']}\nSummary: {summary['summary']}\n")
