from tools.web_search_tool import web_search

def generate_topic(llm, company_context):
    print("Generating topic...")

    trend_data = web_search("latest business trends India OR festivals OR startup news")

    prompt = f"""
    You are an AI content strategist.

    Based on the following Company Context: 
    {company_context}
     
    Generate 10 Instagram post topics.

    IMPORTANT:
    - Return ONLY the topics
    - One topic per line
    - No numbering
    - No bullet points
    - No explanations

    Data:
    {trend_data}
    """

    response = llm.generate(prompt)

    topics = [
        topic.strip()
        for topic in response.split("\n")
        if topic.strip()
    ]
    return topics