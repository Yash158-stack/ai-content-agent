from llm.factory import get_llm
from tools.web_search_tool import web_search
from rag.embeddings import get_embedding
from rag.vector_store import store_data, retrieve_data
from tools.approval_tool import approval_step
from tools.topic_generator import generate_topic
from tools.context_loader import load_company_context
from database.post_repository import save_post

class AgentOrchestrator:
    def __init__(self):
        self.llm = get_llm()
    
    def run(self, topic: str = None):
        print("Agent started...")

        company_context = load_company_context()

        final_topic = topic

        if not final_topic:  
            
            generated_topics = generate_topic(self.llm, company_context)
            print("Generated Topics: \n")

            for i, item in enumerate(generated_topics, start=1):
                print(f"{i}. {item}")

            choice = int(input("\nSelect topic number: "))
            final_topic = generated_topics[choice-1]

        print(final_topic) 

        # Step 1: embed topic (for retrieval)
        query_embedding = get_embedding(final_topic)

        # Step 2: retrieve company knowledge
        retrieved = retrieve_data(query_embedding)

        # Step 3: web search for trends
        search_context = web_search(f"{final_topic} trends OR festive sales OR latest updates")

        # Step 4: store web knowledge
        embedding = get_embedding(search_context)
        store_data(search_context, embedding)

        # Step 5: combine contexts
        rag_context = "\n".join(retrieved)[:1000] if retrieved else ""
        web_context = search_context[:600]

        combined_context = f"""
        Company knowledge:
        {company_context}

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

        Topic: {final_topic}
        """

        response = self.llm.generate(prompt)

        #Step 7: human approval 
        final_content = approval_step(response)

        save_post(
            topic = final_topic,
            content = final_content
        )

        return final_content