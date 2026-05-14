from ddgs import DDGS
from utils.text_cleaner import process_search_results

def web_search(query: str, max_results: int = 5):
    print("Searching the web...")

    raw_results = []

    with DDGS() as ddgs:
        search_results = ddgs.text(query, max_results=max_results)
        
        for r in search_results:
            raw_results.append(r["body"])
    return process_search_results(raw_results)
    