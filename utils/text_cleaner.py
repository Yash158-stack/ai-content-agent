import re

def clean_text(text: str) -> str:
    # remove extra spaces
    text = re.sub(r"\s+", " ", text)

    # remove weired characters
    text = re.sub(r"[^\w\s.,%-]", "", text)

    return text.strip()

def remove_duplicates(text_list):
    seen = set()
    unique = []

    for text in text_list:
        if text not in seen:
            unique.append(text)
            seen.add(text)
    return unique

def process_search_results(results: list, max_chars=1500):
    # clean each result
    cleaned = [clean_text(r) for r in results]

    # remove duplicates
    unique = remove_duplicates(cleaned)

    # combine 
    combined = " ".join(unique)

    # trim size 
    return combined[:max_chars] 

