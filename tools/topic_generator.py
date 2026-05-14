from tools.web_search_tool import web_search

def generate_topic(llm):
    print("Generating topic...")

    trend_data = web_search("latest business trends India OR festivals OR startup news")

    prompt = f"""
    You are an AI content strategist.

    Based on the following data, generate ONE LinkedIn post topic.

    IMPORTANT:
    - Output ONLY the topic
    - Do NOT use placeholders like {{topic}}
    - Do NOT explain anything
    - Do NOT add extra text
    - Keep it short and clear (1 line)

    Example outputs:
    AI adoption in small businesses
    Diwali marketing strategies for startups
    Growth of fintech in India

    Data:
    {trend_data}
    """

    topic = llm.generate(prompt)

    # clean output
    topic = topic.strip()

    # fallback if bad output
    if not topic or "{" in topic or "}" in topic:
        topic = "Latest trends in business and technology"

    return topic