from llm.factory import get_llm
from tools.web_search_tool import web_search
from rag.embeddings import get_embedding
from rag.vector_store import store_data, retrieve_data
from tools.approval_tool import approval_step
from tools.topic_generator import generate_topic

class AgentOrchestrator:
    def __init__(self):
        self.llm = get_llm()
    
    def run(self, topic: str = None):
        print("Agent started...")

        if not topic:
            topic = generate_topic(self.llm)
            print(f"Generated Topic: {topic}")
        # Step 1: embed topic (for retrieval)
        query_embedding = get_embedding(topic)

        # Step 2: retrieve company knowledge
        retrieved = retrieve_data(query_embedding)

        # Step 3: web search for trends
        search_context = web_search(f"{topic} trends OR festival OR latest updates")

        # Step 4: store web knowledge
        embedding = get_embedding(search_context)
        store_data(search_context, embedding)

        # Step 5: combine contexts
        rag_context = "\n".join(retrieved)[:1000] if retrieved else ""
        web_context = search_context[:600]

        combined_context = f"""
        Company knowledge:
        {rag_context}

        Latest trends:
        {web_context}
        """

        # Step 6: generate post
        prompt = f"""
        You are creating a Instagram post for a company.

        STRICT RULES:
        - Max 80–120 words
        - No placeholders

        Use:
        - company knowledge for brand messaging

        Context:
        {combined_context}

        Topic: {topic}
        """

        response = self.llm.generate(prompt)

        #Step 7: human approval 
        final_content = approval_step(response)

        return final_content