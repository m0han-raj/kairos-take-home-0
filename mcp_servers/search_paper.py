import requests
import xml.etree.ElementTree as ET

def search_for_paper(query:str , max_results:int=5):
    url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results={max_results}"
    response = requests.get(url)
    root = ET.fromstring(response.content)

    ns = {"atmo":"http://www.w3.org/2005/Atom"}
    papers=[]
    for entry in root.findall("atmo:entry", ns):
        title = entry.find("atmo:title", ns).text
        pdf_url = entry.find("atmo:link[@type='application/pdf']", ns).get("href")
        papers.append({"title": title, "pdf_link": pdf_url})
    return papers


"""<feed xmlns="http://www.w3.org/2005/Atom">
  <entry>
    <title>Quantum Computing for Beginners</title>
    <link href="https://arxiv.org/pdf/1234.5678.pdf"  type="application/pdf"/>
  </entry>
  <entry>
    <title>An Introduction to Quantum Algorithms</title>
    <link href="https://arxiv.org/pdf/9876.5432.pdf"  type="application/pdf"/>
  </entry>
</feed>"""
# this is given as example to understand the above give code